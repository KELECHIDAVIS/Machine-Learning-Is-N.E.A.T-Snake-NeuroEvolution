import pygame

SCREEN_WIDTH= 800
SCREEN_HEIGHT = 800
FPS = 60

gridCount = 24
gridWidth = SCREEN_WIDTH / gridCount
gridHeight = SCREEN_HEIGHT / gridCount

MOVE_DELAY = 250

clock = pygame.time.Clock()

MAX_GENERATIONS = 2400
MAX_LIFETIME = 9000 #how much update each snake gets
MAX_STEPS_WITHOUT_FOOD = 160
DEATH_SCORE= -5
EAT_SCORE = 10
LIVING_SCORE = -.05
def handle_quadrant(snake_list, state_queue, grid_count, grid_width, screen_width, screen_height):
    for snake in snake_list:
        state_queue.put(snake.update(grid_count, grid_width, screen_width, screen_height))


#draw a bunch of lines instead of drawing a bunch of squares
#where the lines intersect are possible coordinates
def drawGrid(screen):
    #grWidth= width/ gridcount
    #for gc -1: line @ grWidth*i
    for i in range(1, gridCount):
        pygame.draw.line(screen, "gray", (gridWidth*i , 0 ), (gridWidth*i , screen.get_width()), 1)
        pygame.draw.line(screen, "gray", (0 , gridHeight*i ), (screen.get_width() , gridHeight*i), 1)


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

    return True