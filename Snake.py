import random
import pygame
from helper import DEATH_SCORE , LIVING_SCORE, EAT_SCORE, SCREEN_WIDTH, SCREEN_HEIGHT, gridWidth, gridCount, gridHeight, MAX_STEPS_WITHOUT_FOOD


class Link:
    def __init__(self, x , y ):
        self.x = x
        self.y = y
        # self.link = None # We won't need a linked list for drawing anymore if we use a list of positions

'''
each snake agent will have their own food and score and will not interact with one another
'''
class Food:
    def __init__(self, snakeHead_x, snakeHead_y, snake_body_positions): # Pass relevant snake info
        max_attempts = 100  # Limit attempts to prevent infinite loops
        attempt_count = 0
        found_position = False

        while not found_position and attempt_count < max_attempts:
            self.x = random.randint(0, gridCount - 1)
            self.y = random.randint(0, gridCount - 1)

            is_on_snake = False
            # Check if food is on the head
            if self.x == snakeHead_x and self.y == snakeHead_y:
                is_on_snake = True
            else:
                # Check if food is on any body part
                for bx, by in snake_body_positions: # Check against the efficient list
                    if self.x == bx and self.y == by:
                        is_on_snake = True
                        break

            if not is_on_snake:
                found_position = True
            attempt_count += 1

        if not found_position:
            # Fallback: if no suitable position found, place it off-screen
            self.x = -1
            self.y = -1
            print("Warning: Could not find a suitable food position on grid.")


class Snake:
    def __init__(self , x , y ,id ):
        self.x = x # Head X
        self.y = y # Head Y
        self.xVel = 0
        self.yVel = 0
        self.body_positions = [] # List to store (x, y) tuples of body parts
        self.food = Food(self.x, self.y, self.body_positions) # Initialize food with head and body
        self.score = 0
        self.alive = True
        self.id = id
        self.steps_without_food = 0

        # initialize vels: cant either move vertically or horizontally at once
        possible = [1, -1]
        if random.random() > 0.5:
            self.xVel = possible[random.randint(0, 1)]
            self.yVel = 0
        else:
            self.xVel = 0
            self.yVel = possible[random.randint(0, 1)]

    def draw(self , screen):
        # Draw head
        pygame.draw.rect(screen, "green", (self.x*gridWidth, self.y*gridHeight, gridWidth, gridWidth))
        # Draw food
        pygame.draw.rect(screen, "red", (self.food.x*gridWidth, self.food.y*gridHeight, gridWidth, gridWidth))
        # Draw body parts (using the pre-maintained list)
        for bodyPart_x, bodyPart_y in self.body_positions:
            pygame.draw.rect(screen, "brown", (bodyPart_x * gridWidth, bodyPart_y * gridHeight, gridWidth, gridWidth))

    def update(self , network, genome, modify=True):
        self.decide_action(network)
        prevX , prevY = self.move()

        #add determined fitness value
        fitness= self.check_collisions(prevX, prevY)
        if type(genome) == tuple and modify:
            genome[1].fitness+=fitness
        elif modify:
            genome.fitness+=fitness

    # where the thinking occurs
    #takes in a feedforward network and changes vel based on input
    def decide_action(self, network):
        if not self.alive:
            return
        #input: xVel, yVel, foodX, foodY, leftDistanceToObstacle, rightDistToOb, updist, down

        # Obstacle distances
        left_ob_dist = self.x
        right_ob_dist = (gridCount - 1) - self.x # Distance to right wall
        up_ob_dist = self.y
        down_ob_dist = (gridCount - 1) - self.y # Distance to bottom wall

        # Check for body parts as obstacles
        for bx, by in self.body_positions:
            if self.y == by: # Same row
                if bx < self.x: # To the left
                    left_ob_dist = min(left_ob_dist, self.x - bx -1) # Distance to body part
                elif bx > self.x: # To the right
                    right_ob_dist = min(right_ob_dist, bx - self.x -1)
            if self.x == bx: # Same column
                if by < self.y: # Up
                    up_ob_dist = min(up_ob_dist, self.y - by -1)
                elif by > self.y: # Down
                    down_ob_dist = min(down_ob_dist, by - self.y -1)

        # Normalize distances to be more useful for the network (e.g., as a ratio of gridCount)
        # Or you can keep them as raw distances depending on how you've trained your network
        # For now, let's keep them as raw distances. Ensure they are non-negative.
        left_ob_dist = max(0, left_ob_dist)
        right_ob_dist = max(0, right_ob_dist)
        up_ob_dist = max(0, up_ob_dist)
        down_ob_dist = max(0, down_ob_dist)


        #the food position relative to snake
        food_x_relative = self.food.x - self.x
        food_y_relative = self.food.y - self.y

        # Output: (left, right, up, down)
        output = network.activate ((self.xVel, self.yVel, food_x_relative, food_y_relative,
                                    left_ob_dist, right_ob_dist, up_ob_dist, down_ob_dist))

        #find the max index in output list then change vel based on that
        max_index = 0
        for index in range(len(output)):
            if output[max_index ] < output[index]:
                max_index = index

        # Prevent immediate reversal
        if max_index == 0 and self.xVel != 1: # Try to go left
            self.xVel = -1
            self.yVel = 0
        elif max_index == 1 and self.xVel != -1: # Try to go right
            self.xVel = 1
            self.yVel = 0
        elif max_index == 2 and self.yVel != 1: # Try to go up
            self.xVel = 0
            self.yVel = -1
        elif max_index == 3 and self.yVel != -1: # Try to go down
            self.xVel = 0
            self.yVel = 1
        # If the chosen direction is a reversal, the snake maintains its current velocity.
        # This is important for not letting the snake kill itself immediately.
        # This might need fine-tuning with your NEAT setup and desired behavior.


    #move snake by incrementing snake
    def move(self):
        if not self.alive:
            return None, None # Return None if not alive to avoid errors

        prevX = self.x
        prevY = self.y

        # Update body positions: Each segment moves to the previous segment's position
        # The last segment gets the position of the one before it, etc.
        # The first segment (tail) gets the position of the head's previous position.
        if self.body_positions: # Only if snake has a body
            # Make a copy of body_positions for safe iteration
            # This is to avoid issues with modifying a list while iterating it.
            old_body_positions = list(self.body_positions)
            for i in range(len(self.body_positions) - 1, 0, -1):
                self.body_positions[i] = old_body_positions[i-1]
            self.body_positions[0] = (prevX, prevY) # First body part takes head's old position

        self.x += self.xVel
        self.y += self.yVel
        return prevX, prevY

    #check if the snake move into wall, into itself, or with a food
    #if ran into food return 10 fitness
    #if ran into wall or body return -5
    #if didn't crash into anything return -.1
    def check_collisions(self, prevX, prevY):
        if not self.alive:
            return DEATH_SCORE

        # Wall collision
        if self.x < 0 or self.x >= gridCount or self.y < 0 or self.y >= gridCount: # Use gridCount for bounds
            self.alive = False
            return DEATH_SCORE

        # Self-collision
        if (self.x, self.y) in self.body_positions:
            self.alive = False
            return DEATH_SCORE

        # Food collision
        if self.x == self.food.x and self.y == self.food.y:
            self.score += 1
            # Add new link at the current prevX, prevY (the position where the head *was*)
            self.body_positions.insert(0, (prevX, prevY)) # Add to the beginning of the list
            self.food = Food(self.x, self.y, self.body_positions) # New food position, passing updated snake info
            self.steps_without_food = 0
            return EAT_SCORE
        else:
            self.steps_without_food += 1
            if self.steps_without_food > MAX_STEPS_WITHOUT_FOOD:
                self.alive = False
                return DEATH_SCORE

        return LIVING_SCORE

    # We no longer need this if we use self.body_positions list
    # def addLink(self, screen_width, screen_height ):
    #     currLink = self
    #     while currLink.link is not None:
    #         currLink = currLink.link
    #     currLink.link = Link(screen_width,screen_height) # spawn off screen so that it doesn't possibly collide

    def getState(self):
        return {
            "head": (self.x, self.y),
            "body": self.body_positions, # Return the efficient list
            "food": (self.food.x, self.food.y),
            "score": self.score,
            "alive": self.alive,
            "id": self.id
        }

    # This function is no longer needed as body_positions directly stores the body parts
    # def getBodyParts(self):
    #     part_list = []
    #     next_link = self.link
    #     while next_link is not None:
    #         part_list.append((next_link.x, next_link.y))
    #         next_link = next_link.link
    #     return part_list