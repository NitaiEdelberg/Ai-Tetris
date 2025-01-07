from eckity.algorithms import simple_evolution
from eckity.algorithms import Algorithm
from eckity.population import Population
from eckity.subpopulation import Subpopulation
from eckity.creators import creator
from eckity.individual import Individual
from eckity.fitness import Fitness
from eckity.termination_checkers import TerminationChecker
from eckity.genetic_operators.crossovers.vector_k_point_crossover import VectorKPointsCrossover
from eckity.genetic_operators.mutations.vector_random_mutation import FloatVectorGaussNPointMutation

import eckity.genetic_operators.mutations.erc_mutation
from eckity.genetic_operators.selections import tournament_selection
from AIPlayer.AIAgent import AIAgent
from Gameplay.GameSetup import run_tetris_game  # You need to implement this to simulate a game

class TetrisGeneticAlgorithm:
    def __init__(self, population_size=50, generations=5):
        self.population_size = population_size
        self.generations = generations

    def run(self):
        class TetrisFitness(Fitness):
            def __init__(self):
                super().__init__(maximize=True)

            def evaluate(self, individual):
                # Use individual weights in the Tetris game simulation
                weights = individual.vector
                ai_agent = AIAgent(*weights)

                # Simulate the game and return the score
                game_result = run_tetris_game(ai_agent)  # Implement this function
                return game_result['score']  # Return a fitness metric (e.g., score)

        # Set up the evolutionary algorithm
        evolution = Algorithm(
            population=Population(
                sub_populations=[
                    Subpopulation(
                        creators=creator(vector_size=4, lower_bound=-1.0, upper_bound=1.0),
                        population_size=self.population_size,
                        elitism_rate=0.1,
                        fitness=TetrisFitness(),
                        mutation_operator=FloatVectorGaussNPointMutation(),
                        crossover_operator=VectorKPointsCrossover(),
                        selection_operator=tournament_selection(tournament_size=3)
                    )
                ]
            ),
            termination_condition=TerminationChecker(self.generations)
        )

        # Run the genetic algorithm
        evolution.evolve()

        # Get the best individual
        best_individual = evolution.best_individual()
        print("Best Weights:", best_individual.vector)
        return best_individual.vector

# Example usage
if __name__ == "__main__":
    ga = TetrisGeneticAlgorithm(population_size=50, generations=50)
    best_weights = ga.run()
    print("Optimized Weights for AI Agent:", best_weights)
