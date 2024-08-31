import neat
from simulation import run_simulation
from config import load_config
from time import sleep


def main():
    """
    Main entry point for the NEAT car simulation.
    """
    # Load configuration
    config = load_config("./config.txt")

    # Create population and add reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Run simulation for a maximum of 1000 generations
    population.run(run_simulation, 1000)


if __name__ == "__main__":
    sleep(3)
    main()
