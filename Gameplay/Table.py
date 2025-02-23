import numpy as np
from Gameplay import Definitions

class Table:
    """
    The Table class represents the Tetris game board and manages the state of the game.
    """

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
        self.holes_before = 0

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
        self.game_over = not self.can_move(self.current_shape, self.shape_position)

    def rotate(self) -> bool:
        """
        Rotate the current shape 90 degrees counterclockwise.

        :return: True if rotate operation was successful, False if not
        """
        if self.current_shape is not None:
            rotated_shape = np.rot90(self.current_shape)
            self.shape_orientation = (self.shape_orientation + 90) % 360
            if self.can_move(rotated_shape, self.shape_position):
                self.current_shape = rotated_shape
                return True
            else:
                return False

    def shift_right(self) -> bool:
        """
        Shift the current shape right on the board.

        :return: True if shift right operation was successful, False if not
        """
        if self.current_shape is not None:
            new_position = (self.shape_position[0], self.shape_position[1] + 1)
            if self.can_move(self.current_shape, new_position):
                self.shape_position = new_position
                return True
            else:
                return False

    def shift_left(self) -> bool:
        """
        Shift the current shape left on the board.

        :return: True if shift left operation was successful, False if not
        """
        if self.current_shape is not None:
            new_position = (self.shape_position[0], self.shape_position[1] - 1)
            if self.can_move(self.current_shape, new_position):
                self.shape_position = new_position
                return True
            else:
                return False

    def drop(self) -> bool:
        """
        Shift the current shape down on the board.

        :return: True if drop operation was successful, False if not
        """
        if self.current_shape is not None:
            new_position = (self.shape_position[0] + 1, self.shape_position[1])
            if self.can_move(self.current_shape, new_position):
                self.shape_position = new_position
            else:
                self.place_shape()
        return True

    def shape_reposition(self, new_position, new_shape_orientation, reset_shape_landed = False) -> bool:
        """
        Move the current shape to the specified position and orientation.

        :param new_position: (row, col) to which the shape should be moved.
        :param new_shape_orientation: An integer (0, 90, 180, 270) denoting the target orientation.
        :param reset_shape_landed: If true, reset shape landed flag.
        :return: True if shape reposition was successful, False if not.
        """
        if reset_shape_landed:
            self._shape_landed = False

        if self.current_shape is None:
            return False
        else:
            # Calculate how many rotations we need
            offset_degrees = (new_shape_orientation - self.shape_orientation) % 360
            rotations_needed = offset_degrees // 90

            # Save old shape, orientation and position to revert if necessary
            old_shape = self.current_shape.copy()
            old_orientation = self.shape_orientation
            old_position = self.shape_position

            # Perform the required number of rotations, storing the result each time
            rotated_shape = self.current_shape
            for _ in range(rotations_needed):
                rotated_shape = np.rot90(rotated_shape)

            # Check if we can place the newly rotated shape at new_position
            is_valid = self.can_move(rotated_shape, new_position)
            if is_valid:
                self.current_shape = rotated_shape
                self.shape_position = new_position
                self.shape_orientation = new_shape_orientation
            else:
                # If placement is invalid, revert
                self.current_shape = old_shape
                self.shape_position = old_position
                self.shape_orientation = old_orientation

            return is_valid

    def can_move(self, shape, position) -> bool:
        """
        Check if a shape can be moved to a specific position.

        :param shape: The shape to move.
        :param position: A tuple (row, col) of the top-left corner.
        :return: True if the shape can be moved, False otherwise.
        """
        if shape is None:
            return True

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
        self.holes_before = self.get_holes()

        for r in range(self.current_shape.shape[0]):
            for c in range(self.current_shape.shape[1]):
                if self.current_shape[r, c]:
                        self.board[row + r, col + c] = 1 if self.current_shape_name == 'I' else self.current_shape[1, 1]

        self.current_shape = None
        self.current_shape_name = None
        self._shape_landed = True
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

    def board_copy(self) -> np.ndarray:
        """
        Get current board copy.

        :return: A copy of the current board.
        """
        temp_board = self.board.copy()
        if self.current_shape is not None:
            row, col = self.shape_position
            for r in range(self.current_shape.shape[0]):
                for c in range(self.current_shape.shape[1]):
                    if self.current_shape[r, c]:
                        self.board[row + r, col + c] = 1 if self.current_shape_name == 'I' else self.current_shape[1, 1]

        return temp_board

    def is_shape_landing(self) -> bool:
        """
        Check if the current shape has landed.

        :return: True if the current shape has landed, False otherwise.
        """
        return self._shape_landed

    def check_for_cleared_rows(self) -> bool:
        """
        Check how many rows have been cleared.

        :return: Number of cleared rows.
        """
        temp = self._rows_cleared
        self._rows_cleared = 0
        return temp

    def get_bumpiness(self) -> int:
        """
        Calculate the bumpiness of the board.
        Bumpiness is the sum of height differences between adjacent columns.

        :return: Total bumpiness
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

    def get_max_height(self) -> int:
        """
        Calculate the maximum height of the board.

        :return: Maximum column height.
        """
        max_height = 0

        for col in range(self.cols):
            for row in range(self.rows):
                if self.board[row][col] != 0 and max_height < self.rows - row:
                    max_height = self.rows - row
                    break

        return max_height


    def get_holes(self) -> int:
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

    def get_statistics(self) -> dict:
        """
        Return all relevant board statistics for heuristic evaluation.

        :return: Dictionary of board statistics.
        """
        return {
            'bumpiness': self.get_bumpiness(),
            'max_height': self.get_max_height(),
            'holes': self.get_holes(),
            'cleared': self._rows_cleared
        }


def main():
    # For testing how the shapes

    # Create the Tetris table
    tetris = Table()

    # Spawn the shape
    tetris.spawn_next_shape()

    # Display the initial state
    print(tetris.board_copy())

    # Rotate the shape
    tetris.rotate()
    print(tetris.board_copy())

    # Shift the shape right
    tetris.shift_right()
    print(tetris.board_copy())

    # Drop the shape
    tetris.drop()
    print(tetris.board_copy())

    # Shift the shape left
    tetris.shift_right()
    print(tetris.board_copy())

    for i in range(Definitions.BOARD_HEIGHT):
        print(i)
        tetris.drop()
        print(tetris.board_copy())
        land = tetris.is_shape_landing()
        print("Shape landed!")
        if land:
            break


    tetris.spawn_next_shape()
    print(tetris.board_copy())



if __name__ == '__main__':
    main()