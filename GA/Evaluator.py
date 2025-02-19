import random

from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
from eckity.fitness import Fitness
from Gameplay.GameSetup import run_tetris_game
from AIPlayer.AIAgent import AIAgent

class Evaluator(SimpleIndividualEvaluator):
    def __init__(self):
        super().__init__()

    @staticmethod
    def evaluate_individual(individual ,rounds = 5):
        # Use individual weights in the Tetris game simulation
        weights = individual.weights
        ai_agent = AIAgent(*weights)

        # Simulate the game and return the score
        avg_score = 0
        for i in range(rounds):
            avg_score += run_tetris_game(ai_agent=ai_agent, max_moves=1000)
        return avg_score/rounds # Return a fitness metric (e.g. average score)

