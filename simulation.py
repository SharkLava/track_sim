import sys
import pygame
import neat
from car import Car
from config import WIDTH, HEIGHT

current_generation = 0


def run_simulation(genomes, config):
    """
    Run the simulation for one generation of cars.

    :param genomes: List of genomes for this generation
    :param config: NEAT configuration
    """
    global current_generation
    current_generation += 1

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    nets = []
    cars = []

    for _, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
        cars.append(Car())

    game_map = pygame.image.load("./rahul_map.png").convert()
    font = pygame.font.SysFont("Arial", 30)

    counter = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        still_alive = 0
        for i, car in enumerate(cars):
            if car.is_alive():
                still_alive += 1
                car.update(game_map)
                genomes[i][1].fitness += car.get_reward()

                # Get neural network output
                output = nets[i].activate(car.get_data())
                choice = output.index(max(output))

                if choice == 0:
                    car.angle += 10
                elif choice == 1:
                    car.angle -= 10
                elif choice == 2:
                    if car.speed - 2 >= 12:
                        car.speed -= 2
                else:
                    car.speed += 2

        if still_alive == 0:
            break

        counter += 1
        if counter == 30 * 40:  # Stop after about 20 seconds
            break

        _draw_screen(screen, game_map, cars, still_alive, font, counter)
        clock.tick(60)


def _draw_screen(screen, game_map, cars, still_alive, font, counter):
    """
    Draw the game screen.

    :param screen: Pygame screen object
    :param game_map: Game map surface
    :param cars: List of car objects
    :param still_alive: Number of cars still alive
    :param font: Pygame font object
    """
    screen.blit(game_map, (0, 0))
    for car in cars:
        if car.is_alive():
            car.draw(screen)

    text = font.render(f"Generation: {current_generation}", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (100, 10)
    screen.blit(text, text_rect)

    text = font.render(f"Alive: {still_alive}", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (100, 50)
    screen.blit(text, text_rect)

    pygame.display.flip()
