import random

from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
from eckity.fitness import Fitness
from Gameplay.GameSetup import run_tetris_game
from AIPlayer.AIAgent import AIAgent
game_result = 0

class Evaluator(SimpleIndividualEvaluator):
    def __init__(self):
        super().__init__()

    @staticmethod
    def evaluate_individual(individual):
        # Use individual weights in the Tetris game simulation
        weights = individual.weights
        ai_agent = AIAgent(*weights)

        # Simulate the game and return the score
        game_result = run_tetris_game(ai_agent=ai_agent)
        return game_result # Return a fitness metric (e.g., score)

