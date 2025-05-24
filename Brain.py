import random
import pygame
class Brain_Random():

    #returns x and y velocities
    def think(self):
        # initialize vels: cant either move vertically or horizontally at once
        possible = [1, -1]  # vels can be one or neg 1
        if random.random() > 0.5:
            return possible[random.randint(0, 1)] , 0
        else:
            return 0,  possible[random.randint(0, 1)]



class Brain_Manual():
    def think(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return (0, -1)
                if event.key == pygame.K_DOWN:
                    return 0, 1
                if event.key == pygame.K_RIGHT:
                    return 1, 0
                if event.key == pygame.K_LEFT:
                    return -1, 0
