import multiprocessing

from eckity.evaluators.simple_population_evaluator import SimplePopulationEvaluator
from eckity.population import Population

from GA.Evaluator import Evaluator
from GA.Genetics import WeightIndividual
from Gameplay import Definitions

class PopulationEvaluator(SimplePopulationEvaluator):
    """
    A population evaluator that evaluates all individuals in a population
    using multiprocessing for faster computation.
    """

    def __init__(self):
        """
        Initialize the population evaluator.
        """
        super().__init__()

    def act(self, payload=None):
        """
        Perform evaluation on the given payload if it is a Population instance.

        :param payload: The data to evaluate, expected to be a Population instance.
        :return: The best evaluated individual if payload is a Population, otherwise None.
        """
        if isinstance(payload, Population):
            return self.evaluate(payload)
        return None

    def evaluate(self, population: Population) -> WeightIndividual:
        """
        Evaluate all individuals in the population using multiprocessing.
        Assign fitness scores and return the best-performing individual.

        :param population: The population containing individuals to evaluate.
        :return: The best-performing individual based on fitness scores.
        """
        # Extract individuals from all subpopulations
        individuals = [
            individual for sub_pop in population.sub_populations for individual in sub_pop.individuals
        ]

        # Use multiprocessing to evaluate individuals
        with multiprocessing.Pool(processes=Definitions.PROCESS_NUM) as pool:
            fitness_scores = pool.map(Evaluator.evaluate_individual, individuals)

        # Assign fitness scores to individuals and track the best one
        best_individual = None
        best_score = float("-inf")

        for individual, fitness_score in zip(individuals, fitness_scores):
            individual.fitness.set_fitness(fitness_score)
            if fitness_score > best_score:
                best_score = fitness_score
                best_individual = individual

        return best_individual
