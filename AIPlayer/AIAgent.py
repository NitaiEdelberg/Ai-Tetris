from numpy.random import random
import random
from AIPlayer.AIBrain import AIBrain

class AIAgent:

    def __init__(self, bumpiness = random.uniform(-1, 0), max_height = random.uniform(-1, 0), holes = random.uniform(-1, 0), cleared_rows = random.uniform(0, 1)):
        self.weights = [bumpiness, max_height, holes, cleared_rows]  # Example weights: bumpiness, max_height, holes, cleared_rows
        self.best_moves = []


    def choose_action(self, table):
        """
        Decide the best action for the current board state based on heuristic weights.
        :param table: Table instance representing the game board.
        """
        best_score = float('-inf')

        if not self.best_moves and (table.current_shape is not None):
            brain = AIBrain(table, self.weights)
            best_score, best_moves = brain.find_best_placement()


        best_action = best_moves.pop()

        if best_action == 'rotate':
            table.rotate()
        elif best_action == 'shift_left':
            table.shift_left()
        elif best_action == 'shift_right':
            table.shift_right()
        elif best_action == 'drop':
            table.drop()
