from collections import deque
from copy import deepcopy
import numpy as np
import json
from datetime import datetime

from Gameplay.Definitions import POINTS_PER_LINE
from Gameplay.Table import Table


class AIBrain:
    def __init__(self, table: Table, weights):
        self.table = table
        self.weights = weights
        self.log_data = {
            'explored_positions': [],
            'scores': [],
            'moves': [],
            'visited_spots': set(),
            'table': []
        }

    def _evaluate_board(self, table):
        """Evaluate the board based on heuristic features."""
        statistics = table.get_statistics()
        score = (
                self.weights[0] * statistics['bumpiness'] +
                self.weights[1] * statistics['max_height'] +
                self.weights[2] * statistics['holes'] +
                self.weights[3] * (POINTS_PER_LINE[statistics['cleared']] / POINTS_PER_LINE[1])
        )
        # Log the evaluation details
        self.log_data['scores'].append({
            'score': score,
            'statistics': statistics
        })
        return score

    def _simulate_action(self, table: Table, action):
        """Simulate an action and return whether the piece has landed."""
        is_valid = False
        if action == 'rotate':
            is_valid = table.rotate()
        elif action == 'left':
            is_valid = table.shift_left()
        elif action == 'right':
            is_valid = table.shift_right()
        elif action == 'drop':
            is_valid = table.drop()

        # Log the position after the action
        self.log_data['explored_positions'].append({
            'action': action,
            'position': (table.shape_position[0], table.shape_position[1]),
            'orientation': table.shape_orientation,
            'landed': table.is_shape_landing()
        })

        return is_valid, table.is_shape_landing(), table.shape_position, table.shape_orientation

    def find_best_placement_bfs(self):
        """Find the best landing position for the current piece using BFS."""
        # Reset log data for new search
        self.log_data = {
            'explored_positions': [],
            'scores': [],
            'moves': [],
            'visited_spots': set(),
            'piece_type': self.table.current_shape_name,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        queue = deque()
        visited = set()
        best_score = float('-inf')
        best_moves = []

        initial_state = deepcopy(self.table)
        initial_pos = initial_state.shape_position
        initial_orientation = initial_state.shape_orientation
        initial_moves = []
        for i in range(initial_state.rows - initial_state.get_max_height() - len(initial_state.current_shape) - 2):
            new_state: Table = deepcopy(initial_state)
            is_valid, has_landed, initial_pos, initial_state = self._simulate_action(new_state, 'drop')
            initial_state: Table = deepcopy(new_state)

        queue.append((initial_state, initial_moves, initial_pos, initial_orientation))

        while queue:
            current_state, moves, position, orientation = queue.popleft()
            state_key = (position[0], position[1], orientation)

            if state_key in visited:
                continue

            visited.add(state_key)
            self.log_data['visited_spots'].add(str(state_key))  # Convert to string for JSON serialization

            for action in ['drop', 'left', 'right', 'rotate']:

                if current_state.current_shape_name == 'O' and action == 'rotate': #Skip O rotations
                    continue

                new_state: Table = deepcopy(current_state)
                is_valid, has_landed, new_pos, new_orientation = self._simulate_action(new_state, action)

                if not is_valid:
                    continue

                new_moves = moves + [action]

                if has_landed:
                    score = self._evaluate_board(new_state)
                    self.log_data['moves'].append({
                        'sequence': new_moves,
                        'final_position': (new_pos[0], new_pos[1]),
                        'orientation': new_orientation,
                        'score': score
                    })
                    if score > best_score:
                        best_score = score
                        best_moves = new_moves
                else:
                    if new_state.current_shape is None:
                        print(new_state)
                        breakpoint()

                    queue.append((new_state, new_moves, new_pos, new_orientation))

        # Save the best result
        self.log_data['best_score'] = best_score
        self.log_data['best_moves'] = best_moves

        # Save to file
        # self._save_log()

        return best_score, best_moves

    def find_best_placement_column_scan(self):
        """Find the best placement by scanning each row and rotation."""
        best_score = float('-inf')
        best_moves = []
        initial_state = deepcopy(self.table)


        # Try all 4 possible rotations (except for 'O' piece that doesn't rotate)
        for rotation in range(4 if initial_state.current_shape_name != 'O' else 1):
            rotated_state = deepcopy(initial_state)
            for _ in range(rotation):
                self._simulate_action(rotated_state, 'rotate')

            # Try all possible column positions

            effective_width = int(np.sum(np.any(rotated_state.current_shape, axis=0)))
            offset = int(np.argmax(np.concatenate((~np.all(rotated_state.current_shape == 0, axis=0), [True]))))
            for col in range(- offset, initial_state.cols - offset - effective_width + 1):
                test_state = deepcopy(rotated_state)
                is_valid = test_state.shape_reposition((0, col), test_state.shape_orientation)

                if not is_valid:
                    continue

                # Drop the piece to the lowest valid position
                has_landed = False
                while not has_landed:
                    has_landed = self._simulate_action(test_state,'drop')[1]

                score = self._evaluate_board(test_state)

                # Track best-scoring move
                if score > best_score:
                    best_score = score
                    best_moves = ['rotate'] * rotation + [
                        'right' if col > initial_state.shape_position[1] else 'left'] * abs(
                        col - initial_state.shape_position[1]) + ['drop'] * (test_state.shape_position[0] + 1)

        return best_score, best_moves


    def _save_log(self):
        """Save the log data to a file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tetris_ai_log_{timestamp}.json"

        # Convert set to list for JSON serialization
        log_data = dict(self.log_data)
        log_data['visited_spots'] = list(log_data['visited_spots'])
        log_data['table'] = np.array(self.table.display_board()).tolist()

        with open(filename, 'w') as f:
            json.dump(log_data, f, indent=2)

    def print_current_log(self):
        """Print the current log data to console."""
        print("\n=== AI Brain Log ===")
        print(f"Piece Type: {self.log_data['piece_type']}")
        print(f"Best Score: {self.log_data['best_score']}")
        print(f"Best Moves: {self.log_data['best_moves']}")
        print(f"Total Positions Explored: {len(self.log_data['explored_positions'])}")
        print(f"Total Unique Spots Visited: {len(self.log_data['visited_spots'])}")
        print("==================\n")