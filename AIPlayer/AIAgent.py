from pickle import EMPTY_LIST
import copy
from numpy.random import random
import random
from AIPlayer.AIBrain import AIBrain

class AIAgent:

    def __init__(self, bumpiness = random.uniform(-10, 0), max_height = random.uniform(-10, 0), holes = random.uniform(-10, 0),cleared_rows = random.uniform(0, 10)):
        self.weights = [bumpiness, max_height, holes, cleared_rows]  # Example weights: bumpiness, max_height, holes, shape_placement,cleared_rows
        self.best_moves = []
        self.last_shape_name = None


    def choose_action(self, table):
        """
        Decide the best action for the current board state based on heuristic weights.
        :param table: Table instance representing the game board.
        """

        best_score = -1

        if len(self.best_moves) == 0 or table.current_shape_name != self.last_shape_name:
            if (table.current_shape_name is None or table.current_shape_name == self.last_shape_name) and len(self.best_moves) != 0:
                print(f"Current shape: {table.current_shape_name} last shape: {self.last_shape_name} moves left:", self.best_moves)

            brain = AIBrain(copy.deepcopy(table), self.weights)
            best_score, self.best_moves = brain.find_best_placement_column_scan()

            self.last_shape_name = table.current_shape_name

        best_action = self.best_moves.pop(0)
        # print(best_action)
        if best_action == 'rotate':
            table.rotate()
        elif best_action == 'left':
            table.shift_left()
        elif best_action == 'right':
            table.shift_right()
        elif best_action == 'drop':
            table.drop()
