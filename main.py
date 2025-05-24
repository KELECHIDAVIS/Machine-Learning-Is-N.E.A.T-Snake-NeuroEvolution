#main.py

import pygame
from helper import *

'''
snake game:
each frame (lock framerate) ,
snake moves "forward"
can only move in directions orthog to current velocity (only can move up or down if alr moving right or left and vice versa)
each link of snake replaces it's parental's links position
if head runs into food, add another link
if head runs into link, kill snake

head can point to a link
links can only point to other links
head -> link -> link

iteratively change head/link position based on prev position of parent link

FOR MULTIPLE SNAKE AGENTS SHOULD DIVIDE POPULATION INTO QUADRANTS THEN OPEN UP MULTIPLE THREADS TO PROCESS THAT SNAKES IN THEIR QUADRANT  
'''


if __name__ == '__main__':
    pygame.init()

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    while running:
        running = handle_events()

        for snake in snakes:
            if snake.alive:
                snake.update()

        screen.fill("black")

        for snake in snakes:
            if snake.alive:
                snake.draw(screen)

        drawGrid(screen)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()



