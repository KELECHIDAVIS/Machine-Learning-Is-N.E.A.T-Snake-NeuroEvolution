import pygame
import random
from SnakeHead import SnakeHead

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

# pygame setup
pygame.init()

windowSize = 840
FPS = 60
gridCount = 32

grWidth = windowSize/ gridCount
grHeight = windowSize/ gridCount
moveDelay = 150  #ms
lastTime = pygame.time.get_ticks()
screen = pygame.display.set_mode((windowSize,windowSize))
clock = pygame.time.Clock()
running = True


clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

snakeHead = SnakeHead(windowSize/2,windowSize/2, gridCount, grWidth)

#draw a bunch of lines instead of drawing a bunch of squares
#where the lines intersect are possible coordinates
def drawGrid(screen, gridCount, grWidth, grHeight):
    #grWidth= width/ gridcount
    #for gc -1: line @ grWidth*i
    for i in range(1, gridCount):
        pygame.draw.line(screen, "gray", (grWidth*i , 0 ), (grWidth*i , screen.get_width()), 1)
        pygame.draw.line(screen, "gray", (0 , grHeight*i ), (screen.get_width() , grHeight*i), 1)


while running:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_UP :
                snakeHead.setVel((0,-1))
            if event.key == pygame.K_DOWN :
                snakeHead.setVel((0,1))
            if event.key == pygame.K_RIGHT  :
                snakeHead.setVel((1,0))
            if event.key == pygame.K_LEFT :
                snakeHead.setVel((-1,0))

    #FPS
    fps = clock.get_fps()

    #UPDATE
    currentTime = pygame.time.get_ticks()
    if currentTime - lastTime > moveDelay:
        #move snake
        snake_alive = snakeHead.update(gridCount, grWidth , windowSize, screen)

        if not snake_alive:
            print("game over")
            running = False

        lastTime = currentTime

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    drawGrid(screen, gridCount, grWidth, grHeight)
    snakeHead.draw(screen, grWidth, grHeight)
    fps_text = font.render(f"FPS: {int(fps)}", True, pygame.Color('white'))
    screen.blit(fps_text, (10, 10))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(FPS)  # limits FPS to 60

pygame.quit()