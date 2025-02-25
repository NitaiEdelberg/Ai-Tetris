import threading
import builtins
import multiprocessing
import logging
from logging.handlers import QueueHandler, QueueListener

from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.subpopulation import Subpopulation
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.fitness.simple_fitness import SimpleFitness
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection

from Genetics import WeightMutation, WeightCrossover, WeightCreator
from GenerationTerminationChecker import GenerationTerminationChecker
from Evaluator import Evaluator
from PopulationEvaluator import PopulationEvaluator

# Global Variables
best_weights = None
ga_done_event = threading.Event()


# ==============================
# Logging Setup
# ==============================
def setup_logging() -> tuple[QueueListener, multiprocessing.Queue]:
    """
    Set up a logging system with a queue to handle logging from multiple threads and processes.

    :return: A tuple containing:
        - listener: A QueueListener that manages log handlers.
        - log_queue: A multiprocessing queue used for logging messages.
    """
    log_queue = multiprocessing.Queue()
    file_handler = logging.FileHandler('test.log')
    console_handler = logging.StreamHandler()

    log_format = logging.Formatter('%(asctime)s - %(processName)s - %(threadName)s - %(message)s')
    file_handler.setFormatter(log_format)
    console_handler.setFormatter(log_format)

    listener = QueueListener(log_queue, file_handler, console_handler)
    listener.start()

    queue_handler = QueueHandler(log_queue)
    root_logger = logging.getLogger()
    root_logger.handlers = []
    root_logger.addHandler(queue_handler)
    root_logger.setLevel(logging.INFO)

    return listener, log_queue


# ==============================
# Genetic Algorithm Class
# ==============================
class TetrisGeneticAlgorithm:
    """
    A genetic algorithm for optimizing AI agents that play Tetris.
    It evolves a population of AI agents using selection, crossover, and mutation.
    """

    def __init__(self, population_size: int = 20, generations: int = 10):
        """
        Initialize the genetic algorithm parameters.

        :param population_size: The number of individuals in the population.
        :param generations: The number of generations to evolve the population.
        """
        self.population_size = population_size
        self.generations = generations
        self.best_individual = None
        self.logger = logging.getLogger(__name__)

    def run(self):
        """
        Run the genetic algorithm to evolve AI agents for playing Tetris.
        The algorithm performs selection, crossover, and mutation to optimize AI performance.
        """
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
                selection_methods=[(TournamentSelection(tournament_size=3, higher_is_better=True), 1)],
                elitism_rate=0.1
            ),
            population_evaluator=PopulationEvaluator(),
            breeder=SimpleBreeder(),
            max_generation=self.generations,
            statistics=BestAverageWorstStatistics(),
            termination_checker=GenerationTerminationChecker(generations_limit=self.generations,
                                                             fitness_threshold=float('inf')),
            max_workers=1
        )

        ga.evolve()
        self.best_individual = ga.execute()
        self.logger.info(f"Best weights: {self.best_individual.weights}")


# ==============================
# Genetic Algorithm Execution
# ==============================
def run_ga():
    """
    Run the genetic algorithm in a separate thread to optimize AI agents.
    It evolves a population and stores the best weights globally.
    """
    global best_weights
    logger = logging.getLogger(__name__)
    logger.info("Starting Genetic Algorithm...\n")

    try:
        ga = TetrisGeneticAlgorithm(population_size=20, generations=10)
        ga.run()
        best_weights = ga.best_individual.weights
        ga_done_event.set()
        logger.info("GA thread completed")
    except Exception as e:
        logger.error(f"Error in GA thread: {str(e)}", exc_info=True)
        raise


def init_process(queue: multiprocessing.Queue):
    """
    Initialize logging for new processes by assigning them a logging queue.

    :param queue: A multiprocessing queue to handle log messages.
    """
    logging.getLogger().handlers = []  # Remove existing handlers
    queue_handler = QueueHandler(queue)
    logging.getLogger().addHandler(queue_handler)
    logging.getLogger().setLevel(logging.INFO)


# ==============================
# Override Print to Use Logging
# ==============================
def print_override(*args, **kwargs):
    """
    Override the built-in print function to log messages using the logging system.

    :param args: The message to be printed.
    :param kwargs: Additional arguments for print (ignored).
    """
    message = ' '.join(map(str, args))
    logging.getLogger().info(message)

builtins.print = print_override

# ==============================
# Main Execution Block
# ==============================
if __name__ == "__main__":
    """
    Main execution block for running the genetic algorithm in a multi-threaded environment.
    It sets up logging, initializes multiprocessing, and starts the genetic algorithm thread.
    """
    listener, log_queue = setup_logging()
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting main program")

        # Set up multiprocessing with logging support
        ctx = multiprocessing.get_context('spawn')
        with ctx.Pool(initializer=init_process, initargs=(log_queue,)) as pool:
            ga_thread = threading.Thread(target=run_ga, name="GA-Thread")
            ga_thread.start()

            try:
                ai_agent = None  # Placeholder for AI agent initialization
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