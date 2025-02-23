import copy
import random

from AIPlayer.AIBrain import AIBrain

class AIAgent:
    """
    AIAgent controls the Tetris game by deciding and executing moves based on
    heuristic evaluations.
    """

    def __init__(self, bumpiness=random.uniform(-1, 0), max_height=random.uniform(-1, 0), holes=random.uniform(-1, 0),
                  cleared_rows=random.uniform(0, 1), search_method="col_scan"):
        """
        Initializes the AI agent with given weights and the chosen search method.

        :param bumpiness: Weight for bumpiness.
        :param max_height: Weight for max height.
        :param holes: Weight for holes.
        :param cleared_rows: Weight for cleared rows.
        :param search_method: "bfs" for BFS search, "col_scan" for column scan.
        """
        if search_method not in ["bfs", "col_scan"]:
            raise ValueError("Invalid search method.")

        self.weights = [bumpiness, max_height, holes, cleared_rows]
        self.search_method = search_method
        self.best_moves = []
        self.last_shape_name = None


    def choose_action(self, table):
        """
        Decide the best action for the current board state based on heuristic weights.

        :param table: Table instance representing the game board.
        """

        # Calculate the next moves, if necessary
        if len(self.best_moves) == 0 or table.current_shape_name != self.last_shape_name:
            if (table.current_shape_name is None or table.current_shape_name == self.last_shape_name) and len(self.best_moves) != 0:
                print(f"Error! unexpected move calculation.")
                print(f"Current shape: {table.current_shape_name} last shape: {self.last_shape_name} moves left:", self.best_moves)

            brain = AIBrain(copy.deepcopy(table), self.weights)

            # Select the search function dynamically
            if self.search_method == "bfs":
                best_score, self.best_moves = brain.find_best_placement_bfs()
            elif self.search_method == "col_scan":
                best_score, self.best_moves = brain.find_best_placement_column_scan()


            self.last_shape_name = table.current_shape_name

        # Preform the best move
        best_action = self.best_moves.pop(0)

        if best_action == 'rotate':
            table.rotate()
        elif best_action == 'left':
            table.shift_left()
        elif best_action == 'right':
            table.shift_right()
        elif best_action == 'drop':
            table.drop()
