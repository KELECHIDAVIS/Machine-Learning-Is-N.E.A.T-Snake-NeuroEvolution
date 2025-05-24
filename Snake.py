import random
import pygame
from helper import SCREEN_WIDTH, SCREEN_HEIGHT, gridWidth, gridCount, gridHeight
from Brain import Brain_Random, Brain_Manual


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
    def __init__(self , x , y , brain=None):
        self.x = x
        self.y = y
        self.xVel = 0
        self.yVel = 0
        self.link = None  # snakeheads have one pointer to trailing link, links link to other links
        self.food = Food(self)
        self.score = 0
        self.alive = True
        self.id = id
        self.brain =  brain# manual, random, or NEAT

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

    def update(self):
        self.decide_action()
        prevX , prevY = self.move()
        self.check_collisions(prevX, prevY)

    # where the thinking occurs
    #should make async
    def decide_action(self):
        xVel, yVel = self.brain.think()
        self.xVel = xVel
        self.yVel = yVel

    #move snake by incrementing snake
    def move(self):
        prevX = self.x
        prevY = self.y
        self.x += self.xVel
        self.y += self.yVel
        return prevX, prevY

    #check if the snake move into wall, into itself, or with a food
    def check_collisions(self, prevX, prevY):
        if self.x < 0 or self.x *gridWidth> SCREEN_WIDTH or self.y < 0 or self.y *gridWidth> SCREEN_HEIGHT:
            self.alive = False
            return

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
                return
            currLink = currLink.link

        #check collision with food
        if self.x == self.food.x and self.y == self.food.y:
            self.score += 1
            self.food = Food(self)  # new rand food
            # add new link
            self.addLink(SCREEN_WIDTH, SCREEN_HEIGHT)


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