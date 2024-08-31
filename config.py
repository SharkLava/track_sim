import neat

# Screen dimensions
WIDTH = 1920
HEIGHT = 1080

# Car dimensions
CAR_SIZE_X = 50
CAR_SIZE_Y = 50

# Colors
BORDER_COLOR = (255, 255, 255, 255)  # White


def load_config(config_path):
    """
    Load the NEAT configuration.

    :param config_path: Path to the configuration file
    :return: NEAT configuration object
    """
    return neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )
