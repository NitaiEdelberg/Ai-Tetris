from eckity.termination_checkers.termination_checker import TerminationChecker

class GenerationTerminationChecker(TerminationChecker):
    """
    A termination checker for the genetic algorithm that determines when to stop evolution
    based on either the number of generations or a fitness threshold.
    """

    def __init__(self, generations_limit, fitness_threshold):
        """
        Initialize the termination checker with stopping criteria.

        :param generations_limit: The maximum number of generations before termination.
        :param fitness_threshold: The fitness score threshold to stop evolution early.
        """
        super().__init__()
        self.generations_limit = generations_limit
        self.fitness_threshold = fitness_threshold

    def should_terminate(self, population, best_individual, gen_number) -> bool:
        """
        Determine whether the genetic algorithm should terminate based on the defined criteria.

        :param population: The current population of individuals in the genetic algorithm.
        :param best_individual: The best-performing individual in the current generation.
        :param gen_number: The current generation number.
        :return: True if the termination criteria are met (either reaching max generations or
                 achieving the fitness threshold), otherwise False.
        """
        return (gen_number >= self.generations_limit or
                best_individual.fitness.get_pure_fitness() >= self.fitness_threshold)

