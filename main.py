#main.py

import pygame
from SnakeHead import SnakeHead
from multiprocessing import Process, Queue
from helper_functions import handle_quadrant
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
    # pygame setup
    pygame.init()

    width = 840
    height = width
    FPS = 60
    gridCount = 32

    grWidth = width / gridCount
    grHeight = width / gridCount
    moveDelay = 150  #ms
    lastTime = pygame.time.get_ticks()
    screen = pygame.display.set_mode((width, width))
    clock = pygame.time.Clock()
    running = True
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)

    snakes= []
    popSize = 2
    for i in range(popSize):
        snakes.append(SnakeHead(width / 2, width / 2, gridCount, grWidth, i))

    #PROCESS STUFF
    #Split population based on process count and each process will handle their quadrants
    process_count = 2

    #ENSURE THE PROCESS COUNT CAN SPLIT POPULATION UP EVENLY
    if popSize % process_count != 0:
        print("Error: Population size must be divisible by process count")
        exit(-1)



    #draw a bunch of lines instead of drawing a bunch of squares
    #where the lines intersect are possible coordinates
    def drawGrid(screen, gridCount, grWidth, grHeight):
        #grWidth= width/ gridcount
        #for gc -1: line @ grWidth*i
        for i in range(1, gridCount):
            pygame.draw.line(screen, "gray", (grWidth*i , 0 ), (grWidth*i , screen.get_width()), 1)
            pygame.draw.line(screen, "gray", (0 , grHeight*i ), (screen.get_width() , grHeight*i), 1)


    #test_snake = SnakeHead(width / 2, width / 2, gridCount, grWidth, i)
    results = []
    while running:
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        #FPS
        fps = clock.get_fps()

        #UPDATE
        currentTime = pygame.time.get_ticks()

        if currentTime - lastTime > moveDelay:
            popAlive = False
            #state = test_snake.update(gridCount, grWidth, width , height)
            state_queue = Queue()
            #split population into groups then process that group
            num_per_group = popSize//process_count
            processes = []
            for i in range(len(snakes)):
                group = snakes[i*num_per_group:(i+1)*num_per_group]
                processes.append(Process(target=handle_quadrant, args=(group, state_queue, gridCount,grWidth, width, height)))

            #start processes
            for p in processes:
                p.start()

            #wait for all to finish
            for p in processes:
                p.join()

            #get results from queue

            results = [state_queue.get() for p in processes]

            #now check if whole population is dead or not
            for object in results:
                if object['alive'] :
                    popAlive = True
                    break
            # if state['alive']:
            #     popAlive = True
            # results=[state]
            if not popAlive:
                running =  False

            lastTime = currentTime

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # RENDER  GAME HERE

        for object in results:
            if object['alive']:
                pygame.draw.rect(screen, (0, 255, 0), (object['head'][0], object['head'][1],grWidth, grWidth))
                pygame.draw.rect(screen, (255, 0, 0), (object['food'][0], object['food'][1],grWidth, grWidth))

                #for each of the body parts
                for part in object['body']:
                    pygame.draw.rect(screen, 'brown', (part[0], part[1], grWidth, grWidth))

        drawGrid(screen, gridCount, grWidth, grHeight)
        fps_text = font.render(f"FPS: {int(fps)}", True, pygame.Color('white'))
        screen.blit(fps_text, (10, 10))

        # flip() the display to put your work on screen
        pygame.display.update()

        clock.tick(FPS)  # limits FPS to 60

    pygame.quit()