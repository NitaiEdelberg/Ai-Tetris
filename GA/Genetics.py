import random

from eckity.fitness import Fitness
from eckity.genetic_operators.genetic_operator import GeneticOperator
from eckity.individual import Individual
from eckity.creators.creator import Creator

class WeightCreator(Creator):
    def __init__(self, population_size, fitness_type):
        super().__init__()
        self.population_size = population_size
        self.fitness_type = fitness_type

    def create_individuals(self, n_individuals, higher_is_better=False):
        # Generate a list of WeightIndividuals
        return [
            WeightIndividual(fitness=self.fitness_type(higher_is_better=higher_is_better))
            for _ in range(n_individuals)
        ]

class WeightIndividual(Individual):
    def __init__(self, fitness):
        super().__init__(fitness)
        self.weights = [random.uniform(-10, 0) for _ in range(3)] + [random.uniform(0, 10)]  # Example: bumpiness, height, holes, cleared rows

    def show(self):
        return self.weights

    def execute(self):
        return self

class WeightCrossover(GeneticOperator):
    def apply(self, individuals):
        i1, i2 = individuals
        midpoint = len(i1.weights) // 2
        child1_weights = i1.weights[:midpoint] + i2.weights[midpoint:]
        child2_weights = i2.weights[:midpoint] + i1.weights[midpoint:]

        i1.weights, i2.weights = child1_weights, child2_weights
        return individuals

class WeightMutation(GeneticOperator):
    def apply(self, individuals):
        for ind in individuals:
            idx = random.randint(0, len(ind.weights) - 1)
            offset = ind.weights[idx]*random.uniform(0.01, 0.1)
            ind.weights[idx] += random.uniform(-offset, offset)  # Small perturbation
        return individuals
