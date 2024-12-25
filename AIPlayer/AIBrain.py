from collections import deque

from numpy.ma.core import shape


class AIBrain:

    def __init__(self, table, weights):
        self.table = table
        self.weights = weights  # Heuristic weights: [bumpiness, max_height, holes]

    def _evaluate_board(self, board):
        """
        Evaluate the board based on heuristic features.
        :param board: Board state to evaluate.
        :return: Heuristic score.
        """
        statistics = self.table.get_statistics()
        return (
                self.weights[0] * statistics['bumpiness'] +
                self.weights[1] * statistics['max_height'] +
                self.weights[2] * statistics['holes'] +
                self.weights[3] * statistics['cleared']
        )

    def _simulate_action(self, current_position, action):
        """
        Simulate an action and return the new piece position, orientation, and validity.
        :param current_position: Current position of the piece (row, col).
        :param action: Action to perform ('rotate', 'left', 'right', 'drop').
        :return: (new_position, new_orientation, is_valid).
        """
        row, col = current_position
        new_position = current_position

        if action == 'rotate':
            self.table.rotate()
        elif action == 'left':
            self.table.shift_left()
        elif action == 'right':
            self.table.shift_right()
        elif action == 'drop':
            self.table.drop()

        new_position = self.table.shape_position
        is_valid = self.table.can_place(self.table.current_shape, new_position)
        return new_position, is_valid

    def find_best_placement(self):
        """
        Use DFS to find the best placement for the current piece and the moves to get there.
        :return: (best_score, best_moves).
        """
        stack = deque()
        initial_position = self.table.shape_position
        stack.append((initial_position, []))  # (position, moves)

        visited = set()
        best_score = float('-inf')
        best_moves = []

        while stack:
            position, moves = stack.pop()

            # Mark as visited
            visited.add(position)

            # Simulate dropping the piece in the current position and evaluate
            self.table.shape_reposition(position)
            if self.table.shape_position != position: # Shape couldn't be placed in the position
                continue

            for i in range(4):
                self.table.rotate()
                moves.append('rotate')

                if not self.table.can_place(self.table.current_shape, position):
                    continue


                score = self._evaluate_board(self.table.board)
                if score > best_score:
                    best_score = score
                    best_moves = moves.copy()

                moves.pop()

            # Add possible actions to the stack
            for action in ['left', 'right', 'drop']:
                new_position, is_valid = self._simulate_action(position, action)
                if is_valid and new_position not in visited:
                    stack.append((new_position, moves + [action]))

        return best_score, best_moves


