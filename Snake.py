#snake.py
import random
import pygame
from helper import DEATH_SCORE , LIVING_SCORE, EAT_SCORE, SCREEN_WIDTH, SCREEN_HEIGHT, gridWidth, gridCount, gridHeight, MAX_STEPS_WITHOUT_FOOD


class Link:
    def __init__(self, x , y ):
        self.x = x
        self.y = y
        self.link = None

'''
each snake agent will have their own food and score and will not interact with one another 
'''
class Food:
    def __init__(self, snakeHead):
        #can't equal snakes coordinates
        self.x = random.randint(0, gridCount-1)
        self.y = random.randint(0, gridCount-1)


        ''' if the part does not have the same coords move onto the next, if they do, give rand coords and start over '''
        currPart = snakeHead
        while currPart is not None:
            if self.x == currPart.x and self.y == currPart.y:
                self.x = random.randint(0, gridCount-1)
                self.y = random.randint(0, gridCount-1)
                currPart = snakeHead # start over
            else:
                currPart = currPart.link

class Snake:
    def __init__(self , x , y ,id ):
        self.x = x
        self.y = y
        self.xVel = 0
        self.yVel = 0
        self.link = None  # snakeheads have one pointer to trailing link, links link to other links
        self.food = Food(self)
        self.score = 0
        self.alive = True
        self.id = id
        self.steps_without_food = 0

        # initialize vels: cant either move vertically or horizontally at once
        possible = [1, -1]  # vels can be one or neg 1
        if random.random() > 0.5:
            self.xVel = possible[random.randint(0, 1)]
            self.yVel = 0
        else:
            self.xVel = 0
            self.yVel = possible[random.randint(0, 1)]

    def draw(self , screen):
        pygame.draw.rect(screen, "green", (self.x*gridWidth, self.y*gridHeight, gridWidth, gridWidth))
        pygame.draw.rect(screen, "red", (self.food.x*gridWidth, self.food.y*gridHeight, gridWidth, gridWidth))
        bodyParts = self.getBodyParts()
        for bodyPart in bodyParts:
            pygame.draw.rect(screen, "brown", (bodyPart[0] * gridWidth, bodyPart[1]  * gridHeight, gridWidth, gridWidth))

    def update(self , network, genome, modify=True):
        self.decide_action(network)
        prevX , prevY = self.move()

        #add determined fitness value
        fitness= self.check_collisions(prevX, prevY)
        if type(genome) == tuple and modify:
            genome[1].fitness+=fitness
        elif modify:
            genome.fitness+=fitness

        print(self.getState())


    # where the thinking occurs
    #takes in a feedforward network and changes vel based on input
    def decide_action(self, network):
        if not self.alive:
            return
        #input: xVel, yVel, foodX, foodY, leftDistanceToObstacle, rightDistToOb, updist, down

        left_ob_dist = self.x
        right_ob_dist = self.x
        up_ob_dist = self.y
        down_ob_dist = self.y

        #while not running into a obstacle, iterate tracker
        parts = self.getBodyParts()

        while (left_ob_dist, self.y) not in parts and left_ob_dist >0 :
            left_ob_dist = left_ob_dist - 1

        while (right_ob_dist, self.y) not in parts and right_ob_dist<SCREEN_WIDTH :
            right_ob_dist = right_ob_dist + 1

        while (self.x , up_ob_dist) not in parts and up_ob_dist >0 :
            up_ob_dist = up_ob_dist - 1

        while (self.x , down_ob_dist) not in parts and down_ob_dist<SCREEN_HEIGHT :
            down_ob_dist = down_ob_dist + 1

        #the food position relative to snake
        food_x = self.food.x - self.x
        food_y = self.food.y - self.y
        #output: (left, right, up, down)
        output = network.activate ((self.xVel, self.yVel, food_x,food_y, left_ob_dist, right_ob_dist, up_ob_dist, down_ob_dist))

        #find the max index in output list then change vel based on that
        max_index = 0
        for index in range(len(output)):
            if output[max_index ] < output[index]:
                max_index = index

        if max_index == 0 :
            self.xVel = -1
            self.yVel = 0
        elif max_index == 1 :
            self.xVel = 1
            self.yVel = 0
        elif max_index == 2 :
            self.xVel = 0
            self.yVel = -1
        else:
            self.xVel = 0
            self.yVel = 1


    #move snake by incrementing snake
    def move(self):
        if not self.alive:
            return
        prevX = self.x
        prevY = self.y
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

        if self.x < 0 or self.x *gridWidth> SCREEN_WIDTH or self.y < 0 or self.y *gridWidth> SCREEN_HEIGHT:
            self.alive = False
            return DEATH_SCORE

        #check collision with itself
        currLink = self.link
        # Update link position also check if the new snake position is within a link, if so kill snake
        # MAY HAVE TO OPTIMIZE THIS MOVING MECHANISM BUT FOR RN ITS FINE
        while currLink is not None:
            nextX = currLink.x
            nextY = currLink.y
            currLink.x = prevX
            currLink.y = prevY
            prevX = nextX
            prevY = nextY
            if self.x == currLink.x and self.y == currLink.y:
                self.alive = False
                return DEATH_SCORE
            currLink = currLink.link

        #check collision with food
        if self.x == self.food.x and self.y == self.food.y:
            self.score += 1
            self.food = Food(self)  # new rand food
            # add new link
            self.addLink(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.steps_without_food = 0
            return EAT_SCORE
        else:
            self.steps_without_food += 1
            if self.steps_without_food > MAX_STEPS_WITHOUT_FOOD:
                self.alive = False
                return DEATH_SCORE

        return LIVING_SCORE


    def addLink(self, screen_width, screen_height ):
        currLink = self
        while currLink.link is not None:
            currLink = currLink.link
        currLink.link = Link(screen_width,screen_height) # spawn off screen so that it doesn't possibly collide

    def getState(self):
        return {
            "head": (self.x, self.y),
            "body": self.getBodyParts(),
            "food": (self.food.x, self.food.y),
            "score": self.score,
            "alive": self.alive,
            "id": self.id
        }

    # returns list of tuples representing body parts of snake (not including head )
    def getBodyParts(self):
        part_list = []
        next_link = self.link
        while next_link is not None:
            part_list.append((next_link.x, next_link.y))
            next_link = next_link.link
        return part_list