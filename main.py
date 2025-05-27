#main.py
import multiprocessing
import os
from Snake import Snake
from helper import *
import neat
from multiprocessing import Pool
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



#evalutating genomes more efficiently in parallel
#
def run_snake_game(genome, config, render=False):
    if render:

        pygame.init()
        font = pygame.font.Font(None, 30)
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        snake= Snake(SCREEN_WIDTH/2 , SCREEN_HEIGHT/2 , genome.key)
        genome.fitness = 0
        network = neat.nn.FeedForwardNetwork.create(genome, config)

        running = True
        last_time = pygame.time.get_ticks()
        life_time = 0
        while running and life_time < MAX_LIFETIME:

            if not snake.alive:
                break

            current_time = pygame.time.get_ticks()

            # update snakes
            if current_time - last_time > MOVE_DELAY:

                if snake.alive:
                    snake.update(network, genome)


                last_time = current_time
                life_time = life_time + 1

            screen.fill("black")

            if snake.alive:
                snake.draw(screen)

            fps = clock.get_fps()
            fps_text = font.render(f"FPS: {int(fps)}", True, pygame.Color('yellow'))
            screen.blit(fps_text, (10, 10))
            drawGrid(screen)
            pygame.display.update()
            clock.tick(FPS)

        pygame.quit()
    else:
        snake = Snake(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, genome.key)
        genome.fitness = 0
        network = neat.nn.FeedForwardNetwork.create(genome, config)

        running = True
        last_time = pygame.time.get_ticks()
        life_time = 0
        while running and life_time < MAX_LIFETIME:

            if not snake.alive:
                break

            current_time = pygame.time.get_ticks()

            # update snakes
            if current_time - last_time > MOVE_DELAY:

                if snake.alive:
                    snake.update(network, genome)

                last_time = current_time
                life_time = life_time + 1
            clock.tick(FPS)
        return genome.fitness


def eval_genome(genome, config): 
    return run_snake_game( genome , config)


#main function is going to take in genomes of snakes
#and continually update and draw all snakes
#determines the fitness of our snakes
#ITERATIVE APPROACH
def main(genomes, config):
    active_genomes = []
    networks= []
    active_snakes =[]

    pygame.init()
    font = pygame.font.Font(None, 30)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    for genome_id, genome in genomes:
        active_snakes.append(Snake(gridCount / 2, gridCount / 2, genome_id) )
        genome.fitness = 0
        active_genomes.append(genome)
        networks.append(neat.nn.FeedForwardNetwork.create(genome, config))

    running = True
    last_time = pygame.time.get_ticks()
    life_time = 0
    while running and life_time < MAX_LIFETIME:
        running = handle_events()

        if len (active_snakes) == 0:
            break

        current_time = pygame.time.get_ticks()

        #update snakes
        if current_time - last_time > MOVE_DELAY:

            for index, snake in enumerate(active_snakes):
                if snake.alive:
                    snake.update(networks[index], genomes[index])
                else:
                    active_snakes.remove(snake) #remove if died
            last_time = current_time
            life_time = life_time +1

        screen.fill("black")

        for snake in active_snakes:
            if snake.alive:
                snake.draw(screen)

        fps = clock.get_fps()
        fps_text = font.render(f"FPS: {int(fps)}", True, pygame.Color('yellow'))
        screen.blit(fps_text, (10, 10))
        drawGrid(screen)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

def run(config_path):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = p.run(pe.evaluate, MAX_GENERATIONS)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    # print('\nOutput:')
    # winner_net = neat.nn.FeedForwardNetwork.create(winner, config)


    # node_names = {-1: 'A', -2: 'B', 0: 'A XOR B'}
    #
    # visualize.draw_net(config, winner, True, node_names=node_names)
    # visualize.draw_net(config, winner, True, node_names=node_names, prune_unused=True)
    # visualize.plot_stats(stats, ylog=False, view=True)
    # visualize.plot_species(stats, view=True)

    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    # p.run(main, 10)
if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
