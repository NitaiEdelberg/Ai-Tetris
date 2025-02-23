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

    def create_individuals(self, n_individuals, higher_is_better=True):
        # Generate a list of WeightIndividuals
        return [
            WeightIndividual(fitness=self.fitness_type(higher_is_better=higher_is_better))
            for _ in range(n_individuals)
        ]

class WeightIndividual(Individual):
    def __init__(self, fitness):
        super().__init__(fitness)
        self.weights = [random.uniform(-1, 0) for _ in range(3)] + [random.uniform(0, 1)]  # Example: bumpiness, height, holes,, cleared rows
        # self.weights = [-0.1803340898754845, -0.0294471755036216, -0.9725055417051492, 0.13392383443427142]  # Example: bumpiness, height, holes, cleared rows

    def show(self):
        return self.weights

    def execute(self):
        return self

class WeightCrossover(GeneticOperator):
    def apply(self, individuals):
        i1, i2 = individuals
        crossover_point = random.randint(1, len(i1.weights) - 1)  # Random crossover point
        child1_weights = i1.weights[:crossover_point] + i2.weights[crossover_point:]
        child2_weights = i2.weights[:crossover_point] + i1.weights[crossover_point:]

        i1.weights, i2.weights = child1_weights, child2_weights
        return individuals

class WeightMutation(GeneticOperator):
    def apply(self, individuals):
        for ind in individuals:
            idx = random.randint(0, len(ind.weights) - 1)
            # Gaussian mutation, mean=0, standard deviation based on the weight
            mutation = random.gauss(0, abs(ind.weights[idx]) * 0.5)  # Adjust standard deviation
            # mutation = random.choice([-0.1,0.1]) * abs(ind.weights[idx])  # Adjust standard deviation
            ind.weights[idx] += mutation
        return individuals
