from collections import deque
from copy import deepcopy
import numpy as np
import json
from datetime import datetime


class AIBrain:
    def __init__(self, table, weights):
        self.table = table
        self.weights = weights
        self.log_data = {
            'explored_positions': [],
            'scores': [],
            'moves': [],
            'visited_spots': set()
        }

    def _evaluate_board(self, table):
        """Evaluate the board based on heuristic features."""
        statistics = table.get_statistics()
        score = (
                self.weights[0] * statistics['bumpiness'] +
                self.weights[1] * statistics['max_height'] +
                self.weights[2] * statistics['holes'] +
                self.weights[3] * statistics['cleared']
        )

        # Log the evaluation details
        self.log_data['scores'].append({
            'score': score,
            'statistics': statistics
        })
        return score

    def _simulate_action(self, table, action):
        """Simulate an action and return whether the piece has landed."""
        if action == 'rotate':
            table.rotate()
        elif action == 'left':
            table.shift_left()
        elif action == 'right':
            table.shift_right()
        elif action == 'drop':
            table.drop()

        # Log the position after the action
        self.log_data['explored_positions'].append({
            'action': action,
            'position': (table.shape_position[0], table.shape_position[1]),
            'orientation': table.shape_orientation,
            'landed': table.is_shape_landing()
        })

        return (table.is_shape_landing(), table.shape_position, table.shape_orientation)

    def find_best_placement(self):
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
        queue.append((initial_state, [], initial_pos, initial_orientation))

        while queue:
            current_state, moves, position, orientation = queue.popleft()
            state_key = (position[0], position[1], orientation)

            if state_key in visited:
                continue

            visited.add(state_key)
            self.log_data['visited_spots'].add(str(state_key))  # Convert to string for JSON serialization

            for action in ['rotate', 'left', 'right', 'drop']:
                new_state = deepcopy(current_state)
                has_landed, new_pos, new_orientation = self._simulate_action(new_state, action)
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
                elif new_state.current_shape is not None:
                    queue.append((new_state, new_moves, new_pos, new_orientation))

        # Save the best result
        self.log_data['best_score'] = best_score
        self.log_data['best_moves'] = best_moves

        # Save to file
        self._save_log()

        return best_score, best_moves

    def _save_log(self):
        """Save the log data to a file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tetris_ai_log_{timestamp}.json"

        # Convert set to list for JSON serialization
        log_data = dict(self.log_data)
        log_data['visited_spots'] = list(log_data['visited_spots'])

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