import random

import pygame

'''
each snake agent will have their own food and score and will not interact with one another 
'''
class Food:
    def __init__(self, snakeX, snakeY, gridCount, gridWidth ):
        #can't equal snakes coordinates
        self.x = gridWidth * random.randint(0, gridCount)
        self.y = gridWidth * random.randint(0, gridCount)

        while(self.x == snakeX and self.y == snakeY):
            self.x = gridWidth * random.randint(0, gridCount)
            self.y = gridWidth * random.randint(0, gridCount)


class Link:
    def __init__(self, x , y ):
        self.x = x
        self.y = y
        self.link = None

class SnakeHead:

    def __init__(self, x, y, gridCount , gridWidth):
        self.x = x
        self.y= y
        self.xVel = 0
        self.yVel = 0
        self.link = None  # snakeheads have one pointer to trailing link, links link to other links
        self.food = Food(self.x, self.y, gridCount, gridWidth)
        self.score = 0

        #initialize vels: cant either move vertically or horizontally at once
        possible = [1, -1] #vels can be one or neg 1
        if random.random() > 0.5:
            self.xVel = possible[random.randint(0,1)]
            self.yVel = 0
        else:
            self.xVel = 0
            self.yVel = possible[random.randint(0, 1)]

    def update(self,gridCount, gridWidth, windowSize):
        prevX = self.x
        prevY = self.y

        self.x += self.xVel*gridWidth
        self.y += self.yVel*gridWidth


        if self.x == self.food.x and self.y == self.food.y:
            self.score += 1
            print("New score: ", self.score)
            self.food = Food(self.x, self.y, gridCount , gridWidth) #new rand food
            #add new link
            self.addLink()

        if self.x >=windowSize or self.x < 0 or self.y >=windowSize or self.y < 0:
            return False #snake died


        #set link to prev pos
        # save curr coords for following link, take on parents coords
        currLink = self.link

        #MAY HAVE TO OPTIMIZE THIS MOVING MECHANISM BUT FOR RN ITS FINE
        while currLink is not None:
            nextX = currLink.x
            nextY = currLink.y
            currLink.x = prevX
            currLink.y = prevY
            prevX = nextX
            prevY = nextY
            currLink = currLink.link

        return True

    def draw(self, screen , gridWidth, gridHeight ):
        pygame.draw.rect(screen, (0,255,0), (self.x, self.y, gridWidth, gridHeight))
        pygame.draw.rect(screen, (255, 0,0), (self.food.x, self.food.y, gridWidth, gridHeight))

        currLink = self.link
        # MAY HAVE TO OPTIMIZE THIS MOVING MECHANISM BUT FOR RN ITS FINE
        while currLink is not None:
            pygame.draw.rect(screen, "brown", (currLink.x, currLink.y, gridWidth, gridHeight))
            currLink = currLink.link

    def setVel ( self , vels):
        self.xVel = vels[0]
        self.yVel = vels[1]

    def addLink(self):
        currLink = self
        while currLink.link is not None:
            currLink = currLink.link
        currLink.link = Link(0,0)