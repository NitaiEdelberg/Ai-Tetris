from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.subpopulation import Subpopulation
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.fitness.simple_fitness import SimpleFitness
from Genetics import WeightMutation, WeightCrossover, WeightIndividual, WeightCreator
from GenerationTerminationChecker import GenerationTerminationChecker
from Evaluator import Evaluator

class TetrisGeneticAlgorithm:
    def __init__(self, population_size=50, generations=5):
        self.population_size = population_size
        self.generations = generations

    def run(self):
        weight_creator = WeightCreator(self.population_size, fitness_type=SimpleFitness)
        ga = SimpleEvolution(
            Subpopulation(
                creators= weight_creator,
                population_size=50,
                evaluator=Evaluator(),
                higher_is_better=True,
                operators_sequence=[
                    WeightCrossover(probability=0.8),
                    WeightMutation(probability=0.2)
                ],
                elitism_rate=0.05  # Retain top 5% individuals
            ),
            breeder=SimpleBreeder(),
            max_generation=100,  # Run for 100 generations
            statistics=BestAverageWorstStatistics(),
            termination_checker=GenerationTerminationChecker(generations_limit=50, fitness_threshold=1000)
        )

        ga.evolve()
        best = ga.execute()
        print("Best weights:", best.weights)

# Example usage
if __name__ == "__main__":
    ga = TetrisGeneticAlgorithm(population_size=1, generations=10)
    best_weights = ga.run()
    print("Optimized Weights for AI Agent:", best_weights)
