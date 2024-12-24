from Table import Table

class AIAgent:
    def __init__(self):
        self.weights = [-1.0, -1.0, -1.0, 2.0]  # Example weights: bumpiness, max_height, holes, cleared rows

    def choose_action(self, table):
        """
        Decide the best action for the current board state based on heuristic weights.
        :param table: Table instance representing the game board.
        """
        best_score = float('-inf')
        best_action = None

        actions = ['drop', 'rotate', 'shift_right', 'shift_left']
        for action in actions:
            simulated_board = self._simulate_action(table, action)
            score = self._evaluate_board(simulated_board, table.get_statistics())
            if score > best_score:
                best_score = score
                best_action = action

        if best_action == 'rotate':
            table.rotate()
        elif best_action == 'shift_left':
            table.shift_left()
        elif best_action == 'shift_right':
            table.shift_right()
        elif best_action == 'drop':
            table.drop()

    def _simulate_action(self, table, action):
        """
        Simulate an action and return the resulting board state.
        :param table: Table instance.
        :param action: Action to simulate.
        :return: Simulated board state.
        """
        # Clone the table and simulate the action
        table_copy = Table(table.rows, table.cols)
        table_copy.board = table.board.copy()
        if action == 'rotate':
            table_copy.rotate()
        elif action == 'shift_left':
            table_copy.shift_left()
        elif action == 'shift_right':
            table_copy.shift_right()
        elif action == 'drop':
            table_copy.drop()
        return table_copy

    def _evaluate_board(self, board, statistics):
        """
        Evaluate the board based on heuristic features.
        :param board: Simulated board state.
        :param statistics: Board statistics.
        :return: Heuristic evaluation score.
        """
        return (
            self.weights[0] * statistics['bumpiness'] +
            self.weights[1] * statistics['max_height'] +
            self.weights[2] * statistics['holes'] +
            self.weights[3] * statistics['cleared']
        )
