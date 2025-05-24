#main.py

import pygame

from Snake import Snake
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
    font = pygame.font.Font(None, 30)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    for i in range(pop_size):
        snakes.append(Snake(gridCount/2 , gridCount/2))
    while running:
        running = handle_events()

        current_time = pygame.time.get_ticks()
        if current_time - last_time >MOVE_DELAY:
            for snake in snakes:
                if snake.alive:
                    snake.update()
            last_time = current_time
        screen.fill("black")

        for snake in snakes:
            if snake.alive:
                snake.draw(screen)

        fps = clock.get_fps()
        fps_text = font.render(f"FPS: {int(fps)}", True, pygame.Color('yellow'))
        screen.blit(fps_text, (10, 10))
        drawGrid(screen)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()



