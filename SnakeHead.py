import random

import pygame

'''
each snake agent will have their own food and score and will not interact with one another 
'''
class Food:
    def __init__(self, snakeHead, gridCount, gridWidth ):
        #can't equal snakes coordinates
        self.x = gridWidth * random.randint(0, gridCount-1)
        self.y = gridWidth * random.randint(0, gridCount-1)


        ''' if the part does not have the same coords move onto the next, if they do, give rand coords and start over '''
        currPart = snakeHead
        while(currPart != None):
            if self.x == currPart.x and self.y == currPart.y:
                self.x = gridWidth * random.randint(0, gridCount-1)
                self.y = gridWidth * random.randint(0, gridCount-1)
                currPart = snakeHead # start over
            else:
                currPart = currPart.link


class Link:
    def __init__(self, x , y ):
        self.x = x
        self.y = y
        self.link = None

class SnakeHead:

    def __init__(self, x, y, gridCount , gridWidth , id ):
        self.x = x
        self.y= y
        self.xVel = 0
        self.yVel = 0
        self.link = None  # snakeheads have one pointer to trailing link, links link to other links
        self.food = Food(self, gridCount, gridWidth)
        self.score = 0
        self.alive = True
        self.id = id

        #initialize vels: cant either move vertically or horizontally at once
        possible = [1, -1] #vels can be one or neg 1
        if random.random() > 0.5:
            self.xVel = possible[random.randint(0,1)]
            self.yVel = 0
        else:
            self.xVel = 0
            self.yVel = possible[random.randint(0, 1)]

    def update(self,gridCount, gridWidth, windowSize, screen):
        if(self.alive):

            prevX = self.x
            prevY = self.y


            #AI should make decisions here
            # initialize vels: cant either move vertically or horizontally at once
            possible = [1, -1]  # vels can be one or neg 1
            if random.random() > 0.5:
                self.xVel = possible[random.randint(0, 1)]
                self.yVel = 0
            else:
                self.xVel = 0
                self.yVel = possible[random.randint(0, 1)]

            self.x += self.xVel*gridWidth
            self.y += self.yVel*gridWidth


            if self.x == self.food.x and self.y == self.food.y:
                self.score += 1
                self.food = Food(self, gridCount , gridWidth) #new rand food
                #add new link
                self.addLink(screen)

            if self.x >=windowSize or self.x < 0 or self.y >=windowSize or self.y < 0:
                self.alive = False
                print(f"Snake {self.id} died with score {self.score} ")
                return self.alive #snake died


            #set link to prev pos
            # save curr coords for following link, take on parents coords
            currLink = self.link

            #Update link position also check if the new snake position is within a link, if so kill snake
            #MAY HAVE TO OPTIMIZE THIS MOVING MECHANISM BUT FOR RN ITS FINE
            while currLink is not None:
                nextX = currLink.x
                nextY = currLink.y
                currLink.x = prevX
                currLink.y = prevY
                prevX = nextX
                prevY = nextY
                if self.x == currLink.x and self.y == currLink.y:
                    self.alive = False
                    print(f"Snake {self.id} died with score {self.score} ")
                    return self.alive # kill snake if it overlaps with body part
                currLink = currLink.link

        return self.alive

    def draw(self, screen , gridWidth, gridHeight ):
        if(self.alive):
            pygame.draw.rect(screen, (0,255,0), (self.x, self.y, gridWidth, gridHeight))
            pygame.draw.rect(screen, (255, 0,0), (self.food.x, self.food.y, gridWidth, gridHeight))

            currLink = self.link
            # MAY HAVE TO OPTIMIZE THIS MOVING MECHANISM BUT FOR RN ITS FINE
            while currLink is not None:
                pygame.draw.rect(screen, "brown", (currLink.x, currLink.y, gridWidth, gridHeight))
                currLink = currLink.link

    def setVel ( self , vels):
        #ensure orthogonality
        if self.xVel != abs(vels[0]) and self.yVel != abs(vels[1]):
            self.xVel = vels[0]
            self.yVel = vels[1]

    def addLink(self, screen ):
        currLink = self
        while currLink.link is not None:
            currLink = currLink.link
        currLink.link = Link(screen.get_width(),screen.get_height()) # spawn off screen so that it doesn't possibly collide

