import threading

from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.subpopulation import Subpopulation
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.fitness.simple_fitness import SimpleFitness

from Gameplay.GameSetup import run_tetris_game
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
                population_size=2,
                evaluator=Evaluator(),
                higher_is_better=True,
                operators_sequence=[
                    WeightCrossover(probability=0.8),
                    WeightMutation(probability=0.2)
                ],
                elitism_rate=0.05  # Retain top 5% individuals
            ),
            breeder=SimpleBreeder(),
            max_generation=10,  # Run for 100 generations
            statistics=BestAverageWorstStatistics(),
            termination_checker=GenerationTerminationChecker(generations_limit=20, fitness_threshold=1000),
            max_workers=1
        )

        ga.evolve()
        best = ga.execute()
        print("Best weights:", best.weights)

# Shared variable for the best weights
best_weights = None
ga_done_event = threading.Event()

def run_ga():
    global best_weights
    ga = TetrisGeneticAlgorithm(population_size=2, generations=10)
    ga.run()
    best_weights = ga.best_individual.weights
    # Set the best weights (replace `None` with the actual result from your GA)
    # best_weights = [0.5, 0.5, 0.5, 0.5]  # Example values
    ga_done_event.set()  # Signal that the GA is done

if __name__ == "__main__":
    # Start the GA in a separate thread
    ga_thread = threading.Thread(target=run_ga)
    ga_thread.start()

    # Run the PyGame loop with a default AI agent
    try:
        ai_agent = None
        # while not ga_done_event.is_set():
        #     # Run PyGame with a default AI or placeholder agent
        #     run_tetris_game(play_with_human=False, ai_agent=ai_agent)

        # Once GA is done, update the AI agent with the best weights
        print("GA completed! Best weights:", best_weights)
        ai_agent = None  # Create a new agent using the best weights
        # run_tetris_game(play_with_human=False, ai_agent=ai_agent)

    finally:
        # Ensure the GA thread finishes
        ga_thread.join()
        print("GA thread has completed.")
