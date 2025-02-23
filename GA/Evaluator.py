from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator

from Gameplay.AIGameSimulator import run_tetris_game
from AIPlayer.AIAgent import AIAgent

class Evaluator(SimpleIndividualEvaluator):
    """
    Evaluator class responsible for evaluating the fitness of AI agents
    based on their performance in the Tetris game.
    """

    def __init__(self):
        """
        Initialize the evaluator.
        """
        super().__init__()


    @staticmethod
    def evaluate_individual(individual ,rounds = 5) -> float:
        """
        Evaluate an individual's fitness by simulating Tetris games and measuring performance.

        :param individual: The individual to be evaluated.
        :param rounds: The number of Tetris games to simulate for averaging the score (default: 5).
        :return: The average score achieved by the AI agent across multiple rounds.
        """
        # Use individual weights in the Tetris game simulation
        weights = individual.weights
        ai_agent = AIAgent(*weights)

        # Simulate the game and return the score
        avg_score = 0
        for i in range(rounds):
            avg_score += run_tetris_game(ai_agent=ai_agent)
            # avg_score += run_tetris_game_with_graphics(ai_agent=ai_agent)
        return avg_score/rounds # Return a fitness metric (e.g. average score)

