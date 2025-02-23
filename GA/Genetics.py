import random

from eckity.genetic_operators.genetic_operator import GeneticOperator
from eckity.individual import Individual
from eckity.creators.creator import Creator

class WeightCreator(Creator):
    """
    A creator class responsible for generating WeightIndividual instances
    to be used in the genetic algorithm.
    """

    def __init__(self, population_size: int, fitness_type: type):
        """
        Initialize the WeightCreator with the population size and fitness type.

        :param population_size: The number of individuals to create in the population.
        :param fitness_type: The type of fitness evaluation to use for individuals.
        """
        super().__init__()
        self.population_size = population_size
        self.fitness_type = fitness_type


    def create_individuals(self, n_individuals, higher_is_better=True):
        """
        Generate a list of WeightIndividuals with random weights.

        :param n_individuals: The number of individuals to create.
        :param higher_is_better: Whether a higher fitness value is considered better.
        :return: A list of WeightIndividual instances.
        """
        return [
            WeightIndividual(fitness=self.fitness_type(higher_is_better=higher_is_better))
            for _ in range(n_individuals)
        ]

class WeightIndividual(Individual):
    """
    Represents an individual in the genetic algorithm, characterized by heuristic weights.
    """

    def __init__(self, fitness):
        """
        Initialize a WeightIndividual with random heuristic weights.

        :param fitness: The fitness evaluation object for this individual.
        """
        super().__init__(fitness)
        self.weights = [random.uniform(-1, 0) for _ in range(3)] + [random.uniform(0, 1)]  # Example weight initialization

    def show(self) -> list[float]:
        """
        Return the individual's weights.

        :return: A list of heuristic weights.
        """
        return self.weights

    def execute(self):
        """
        Return the individual itself.

        :return: The current WeightIndividual instance.
        """
        return self


class WeightCrossover(GeneticOperator):
    """
    A genetic crossover operator that combines the weights of two parent individuals
    to create new offspring.
    """

    def apply(self, individuals: list[WeightIndividual]) -> list[WeightIndividual]:
        """
        Apply crossover between two individuals by swapping part of their weights.

        :param individuals: A list containing two parent individuals.
        :return: A list containing the modified individuals after crossover.
        """
        i1, i2 = individuals
        crossover_point = random.randint(1, len(i1.weights) - 1)  # Random crossover point
        child1_weights = i1.weights[:crossover_point] + i2.weights[crossover_point:]
        child2_weights = i2.weights[:crossover_point] + i1.weights[crossover_point:]

        i1.weights, i2.weights = child1_weights, child2_weights
        return individuals


class WeightMutation(GeneticOperator):
    """
    A genetic mutation operator that modifies the weights of individuals randomly.
    """

    def apply(self, individuals: list[WeightIndividual]) -> list[WeightIndividual]:
        """
        Apply mutation to randomly alter the weights of individuals.

        :param individuals: A list of individuals to be mutated.
        :return: A list of mutated individuals.
        """
        for ind in individuals:
            idx = random.randint(0, len(ind.weights) - 1)
            mutation = random.gauss(0, abs(ind.weights[idx]) * 0.1)  # Apply Gaussian mutation
            ind.weights[idx] += mutation
        return individuals

