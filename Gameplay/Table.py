from logging import raiseExceptions

import numpy as np
from numpy.ma.core import shape, count
from numpy.random import random

import Definitions
from Gameplay.Definitions import SHAPES


class Table:

    def __init__(self, rows=Definitions.BOARD_HEIGHT, cols=Definitions.BOARD_WIDTH):
        """
        Initialize the Tetris table.

        :param rows: Number of rows on the board.
        :param cols: Number of columns on the board.
        """
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols), dtype=int)
        self.current_shape = None
        self.current_shape_name = None
        self.shape_position = (0, 0)  # (row, col)
        self.shape_generator = list(Definitions.SHAPES.keys())
        # self.shape_generator = list('I'*7)
        np.random.shuffle(self.shape_generator)
        self.shape_generator_pos = 0
        self._shape_landed = False
        self._rows_cleared = 0
        self.game_over = False
        self.shape_orientation = 0

    def spawn_next_shape(self):
        """
        Spawn the next shape on the board.
        """
        if self.shape_generator_pos >= len(self.shape_generator):
            np.random.shuffle(self.shape_generator)
            self.shape_generator_pos = 0

        self.current_shape_name = self.shape_generator[self.shape_generator_pos]
        self.current_shape = Definitions.SHAPES[self.current_shape_name]
        self.shape_generator_pos += 1
        self.shape_position = (0, self.cols // 2 - len(self.current_shape) // 2)
        self.shape_orientation = 0
        self._shape_landed = False
        self.game_over = not self.can_place(self.current_shape, self.shape_position)

    def rotate(self):
        """
        Rotate the current shape 90 degrees counterclockwise.
        """
        if self.current_shape is not None:
            rotated_shape = np.rot90(self.current_shape)
            self.shape_orientation = (self.shape_orientation + 90) % 360
            if self.can_place(rotated_shape, self.shape_position):
                self.current_shape = rotated_shape

    def shift_right(self):
        """
        Shift the current shape right on the board.
        """
        if self.current_shape is not None:
            new_position = (self.shape_position[0], self.shape_position[1] + 1)
            if self.can_place(self.current_shape, new_position):
                self.shape_position = new_position

    def shift_left(self):
        """
        Shift the current shape left on the board.
        """
        if self.current_shape is not None:
            new_position = (self.shape_position[0], self.shape_position[1] - 1)
            if self.can_place(self.current_shape, new_position):
                self.shape_position = new_position

    def drop(self):
        """
        Shift the current shape down on the board.
        """
        if self.current_shape is not None:
            new_position = (self.shape_position[0] + 1, self.shape_position[1])
            if self.can_place(self.current_shape, new_position):
                self.shape_position = new_position
            else:
                self._shape_landed = True
                self.place_shape()

    def shape_reposition(self, new_position, new_shape_orientation, reset_shape_landed = False):
        """
        Move the current shape to the specified position and orientation.
        :param new_position: (row, col) to which the shape should be moved.
        :param new_shape_orientation: An integer (0, 90, 180, 270) denoting the target orientation.
        """
        if self.current_shape is not None:
            # 1. Calculate how many 90° rotations we need
            #    E.g., if current shape_orientation=90 and new_shape_orientation=270,
            #    offset = 270 - 90 = 180; times = 180 // 90 = 2
            offset_degrees = (new_shape_orientation - self.shape_orientation) % 360
            rotations_needed = offset_degrees // 90

            # 2. Save old shape/orientation/position to revert if necessary
            old_shape = self.current_shape.copy()
            old_orientation = self.shape_orientation
            old_position = self.shape_position

            # 3. Perform the required number of 90° rotations, storing the result each time
            rotated_shape = self.current_shape
            for _ in range(rotations_needed):
                rotated_shape = np.rot90(rotated_shape)

            # 4. Check if we can place the newly rotated shape at new_position
            if self.can_place(rotated_shape, new_position):
                self.current_shape = rotated_shape
                self.shape_position = new_position
                self.shape_orientation = new_shape_orientation
            else:
                # 5. If placement is invalid, revert
                self.current_shape = old_shape
                self.shape_position = old_position
                self.shape_orientation = old_orientation
        if reset_shape_landed:
            self._shape_landed = False

    def can_place(self, shape, position):
        """
        Check if a shape can be placed at a specific position.

        :param shape: The shape to place.
        :param position: A tuple (row, col) of the top-left corner.
        :return: True if the shape can be placed, False otherwise.
        """
        if shape is None:
            return False

        row, col = position
        for r in range(shape.shape[0]):
            for c in range(shape.shape[1]):
                if shape[r, c]:  # If the cell is part of the shape
                    board_row = row + r
                    board_col = col + c
                    if (board_row < 0 or board_row >= self.rows or
                            board_col < 0 or board_col >= self.cols or
                            self.board[board_row, board_col]):
                        return False
        return True

    def place_shape(self):
        """
        Place the current shape on the board and clear full rows.
        """
        row, col = self.shape_position
        # shape_id = list(Definitions.SHAPES.keys())[self.shape_generator_pos - 1]
        for r in range(self.current_shape.shape[0]):
            for c in range(self.current_shape.shape[1]):
                if self.current_shape[r, c]:
                    if self.current_shape_name == 'I':
                        self.board[row + r, col + c] = 1
                    else:
                        self.board[row + r, col + c] = self.current_shape[1, 1]
        self.current_shape = None
        self._clear_rows()

    def _clear_rows(self):
        """
        Clear full rows on the board.
        """
        full_rows = [r for r in range(self.rows) if all(self.board[r])]
        for row in full_rows:
            self._rows_cleared += 1
            self.board[1:row + 1] = self.board[:row]
            self.board[0] = 0

    def display_board(self):
        """
        Print the current state of the board.
        """
        temp_board = self.board.copy()
        if self.current_shape is not None:
            row, col = self.shape_position
            for r in range(self.current_shape.shape[0]):
                for c in range(self.current_shape.shape[1]):
                    if self.current_shape[r, c]:
                        if self.current_shape_name == 'I':
                            temp_board[row + r, col + c] = 1
                        else:
                            temp_board[row + r, col + c] = self.current_shape[1, 1]
        print(temp_board, end='\n\n')

    def is_shape_landing(self):
        """
        Check if the current shape has landed.
        :return: True if the current shape has landed, False otherwise.
        """
        return self._shape_landed
        # return not self._can_place(self.current_shape, self.shape_position)

    def check_for_cleared_rows(self):
        """
            Check how many rows have been cleared.
            :return: Number of cleared rows.
        """
        temp = self._rows_cleared
        self._rows_cleared = 0
        return temp

    def get_bumpiness(self):
        """
        Calculate the bumpiness of the board.
        Bumpiness is the total difference in heights between adjacent columns.

        :return: Total bumpiness (sum of height differences between adjacent columns).
        """
        column_heights = []
        for col in range(self.cols):
            for row in range(len(self.board)):
                if self.board[row][col] != 0:
                    column_heights.append(self.rows - row)
                    break
            else:
                column_heights.append(0)

        bumpiness = 0
        for i in range(len(column_heights) - 1):
            bumpiness += abs(column_heights[i] - column_heights[i + 1])

        return bumpiness

    def get_aggregate_height(self):
        """
        Calculate the aggregate height of the board.
        :return: Maximum column height.
        """
        aggregate_height = 0

        for col in range(self.cols):
            for row in range(self.rows):
                if self.board[row][col] != 0:
                    aggregate_height += self.rows - row
                    break

        return aggregate_height


    def get_holes(self):
        """
        Count the number of holes in the board.
        :return: Total number of holes (empty cells beneath at least one filled cell).
        """
        holes = 0
        for col in range(self.cols):
            found_block = False
            for row in range(self.rows):
                if self.board[row, col] != 0 and not found_block:
                    found_block = True
                elif self.board[row, col] == 0 and found_block:
                    holes += 1
        return holes

    def get_statistics(self):
        """
        Return all relevant board statistics for heuristic evaluation.
        :return: Dictionary of board statistics.
        """
        return {
            'bumpiness': self.get_bumpiness(),
            'max_height': self.get_aggregate_height(),
            'holes': self.get_holes(),
            'cleared': self._rows_cleared
        }


def main():

    # Create the Tetris table
    tetris = Table()

    # Spawn the shape
    tetris.spawn_next_shape()

    # Display the initial state
    tetris.display_board()

    # Rotate the shape
    tetris.rotate()
    tetris.display_board()

    # Shift the shape right
    tetris.shift_right()
    tetris.display_board()

    # Drop the shape
    tetris.drop()
    tetris.display_board()

    # Shift the shape left
    tetris.shift_right()
    tetris.display_board()

    for i in range(40):
        print(i)
        tetris.drop()
        tetris.display_board()
        land = tetris.is_shape_landing()
        print(land)
        if land:
            tetris.spawn_next_shape()

    tetris.spawn_next_shape()
    tetris.display_board()



if __name__ == '__main__':
    main()