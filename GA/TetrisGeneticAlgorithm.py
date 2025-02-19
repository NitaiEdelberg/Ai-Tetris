import threading
import logging
import multiprocessing
from logging.handlers import QueueHandler, QueueListener
from queue import Queue

import eckity.genetic_operators
from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.subpopulation import Subpopulation
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.fitness.simple_fitness import SimpleFitness
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection

from Gameplay.GameSetup import run_tetris_game
from Genetics import WeightMutation, WeightCrossover, WeightIndividual, WeightCreator
from GenerationTerminationChecker import GenerationTerminationChecker
from Evaluator import Evaluator
from PopulationEvaluator import PopulationEvaluator


def setup_logging():
    # Create a queue for logging
    log_queue = multiprocessing.Queue()

    # Create handlers
    file_handler = logging.FileHandler('test_5p_big_2_bfs.log')
    console_handler = logging.StreamHandler()

    # Create formatters and add it to handlers
    log_format = logging.Formatter('%(asctime)s - %(processName)s - %(threadName)s - %(message)s')
    file_handler.setFormatter(log_format)
    console_handler.setFormatter(log_format)

    # Create queue listener
    listener = QueueListener(log_queue, file_handler, console_handler)

    # Start the listener in a separate thread
    listener.start()

    # Create and configure queue handler
    queue_handler = QueueHandler(log_queue)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.handlers = []  # Remove any existing handlers
    root_logger.addHandler(queue_handler)
    root_logger.setLevel(logging.INFO)

    return listener, log_queue


class TetrisGeneticAlgorithm:
    def __init__(self, population_size=50, generations=5):
        self.population_size = population_size
        self.generations = generations
        self.best_individual = None
        self.logger = logging.getLogger(__name__)

    def run(self):
        weight_creator = WeightCreator(self.population_size, fitness_type=SimpleFitness)
        ga = SimpleEvolution(
            Subpopulation(
                creators=weight_creator,
                population_size=self.population_size,
                evaluator=Evaluator(),
                higher_is_better=True,
                operators_sequence=[
                    WeightCrossover(probability=0.65, arity=2),
                    WeightMutation(probability=0.35, arity=10)
                ],
                selection_methods=[(TournamentSelection(tournament_size= 3,higher_is_better=True), 1)],
                elitism_rate=0.2
            ),
            population_evaluator=PopulationEvaluator(),
            breeder=SimpleBreeder(),
            max_generation=self.generations,
            statistics=BestAverageWorstStatistics(),
            termination_checker=GenerationTerminationChecker(generations_limit=self.generations,
                                                             fitness_threshold=100000),
            max_workers=1
        )
        ga.evolve()
        self.best_individual = ga.execute()
        self.logger.info(f"Best weights: {self.best_individual.weights}")


# Override print to use logging
def print_override(*args, **kwargs):
    message = ' '.join(map(str, args))
    logging.getLogger().info(message)


import builtins

builtins.print = print_override

# Shared variable for the best weights
best_weights = None
ga_done_event = threading.Event()


def run_ga():
    global best_weights
    logger = logging.getLogger(__name__)
    logger.info("Starting Genetic Algorithm...\n")
    try:
        ga = TetrisGeneticAlgorithm(population_size=50, generations=15)
        ga.run()
        best_weights = ga.best_individual.weights
        ga_done_event.set()
        logger.info("GA thread completed")
    except Exception as e:
        logger.error(f"Error in GA thread: {str(e)}", exc_info=True)
        raise


def init_process(queue):
    """Initialize logging for new processes"""
    logging.getLogger().handlers = []  # Remove any existing handlers
    queue_handler = QueueHandler(queue)
    logging.getLogger().addHandler(queue_handler)
    logging.getLogger().setLevel(logging.INFO)


if __name__ == "__main__":
    # Set up logging and get the queue
    listener, log_queue = setup_logging()
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting main program")

        # If your evaluator uses multiprocessing, set it up with logging initialization
        ctx = multiprocessing.get_context('spawn')
        with ctx.Pool(initializer=init_process, initargs=(log_queue,)) as pool:
            ga_thread = threading.Thread(target=run_ga, name="GA-Thread")
            ga_thread.start()

            try:
                ai_agent = None
                # Your game loop code here
                ga_thread.join()
                logger.info("GA completed!")

            except Exception as e:
                logger.error(f"Error in main thread: {str(e)}", exc_info=True)
                raise

            finally:
                if ga_thread.is_alive():
                    ga_thread.join()

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)

    finally:
        logger.info("Program finished\n")
        listener.stop()  # Stop the logging listener
        log_queue.close()  # Close the logging queue