from eckity.evaluators.simple_population_evaluator import SimplePopulationEvaluator
from eckity.fitness import Fitness
from eckity.population import Population
import multiprocessing
import threading
from GA.Evaluator import Evaluator
from Gameplay import Definitions
class PopulationEvaluator(SimplePopulationEvaluator):

    def __init__(self):
        super().__init__()

    def act(self, payload=None):
        if isinstance(payload, Population):
            return self.evaluate(payload)
        return None

    def evaluate(self, population):
        # Extract individuals from all subpopulations
        individuals = [
            individual for sub_pop in population.sub_populations for individual in sub_pop.individuals
        ]

        # Use multiprocessing to evaluate individuals
        with multiprocessing.Pool(processes=Definitions.PROCESS_NUM) as pool:
            fitness_scores = pool.map(Evaluator.evaluate_individual, individuals)

        # Assign fitness scores to individuals
        best_individual = None

        best_score = float("-inf")
        for individual, fitness_score in zip(individuals, fitness_scores):
            individual.fitness.set_fitness(fitness_score)
            if fitness_score > best_score:
                best_individual = individual

        # Return the best individual
        return best_individual