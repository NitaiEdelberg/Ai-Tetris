import numpy as np

class Table:
    _shapes = {
        'I': [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        'J': [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0],
        ],
        'L': [
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0],
        ],
        'O': [
            [1, 1],
            [1, 1],
        ],
        'S': [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0],
        ],
        'Z': [
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0],
        ],
        'T': [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0],
        ]
    }

    def __init__(self, rows=10, cols=10):
        """
        Initialize the Tetris table.

        :param rows: Number of rows on the board.
        :param cols: Number of columns on the board.
        """
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols), dtype=int)
        self.current_shape = None
        self.shape_position = (0, 0)  # (row, col)

    def spawn_shape(self, shape):
        """
        Spawn a new shape on the board.

        :param shape: A 2D numpy array representing the shape.
        """
        self.current_shape = shape
        self.shape_position = (0, self.cols // 2 - shape.shape[1] // 2)

    def rotate(self):
        """
        Rotate the current shape 90 degrees counterclockwise.
        """
        if self.current_shape is not None:
            rotated_shape = np.rot90(self.current_shape)
            if self._can_place(rotated_shape, self.shape_position):
                self.current_shape = rotated_shape

    def shift_right(self):
        """
        Shift the current shape right on the board.
        """
        if self.current_shape is not None:
            new_position = (self.shape_position[0], self.shape_position[1] + 1)
            if self._can_place(self.current_shape, new_position):
                self.shape_position = new_position

    def shift_left(self):
        """
        Shift the current shape left on the board.
        """
        if self.current_shape is not None:
            new_position = (self.shape_position[0], self.shape_position[1] - 1)
            if self._can_place(self.current_shape, new_position):
                self.shape_position = new_position

    def drop(self):
        """
        Shift the current shape down on the board.
        """
        if self.current_shape is not None:
            new_position = (self.shape_position[0] + 1, self.shape_position[1])
            if self._can_place(self.current_shape, new_position):
                self.shape_position = new_position
            else:
                self._place_shape()

    def _can_place(self, shape, position):
        """
        Check if a shape can be placed at a specific position.

        :param shape: The shape to place.
        :param position: A tuple (row, col) of the top-left corner.
        :return: True if the shape can be placed, False otherwise.
        """
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

    def _place_shape(self):
        """
        Place the current shape on the board and clear full rows.
        """
        row, col = self.shape_position
        for r in range(self.current_shape.shape[0]):
            for c in range(self.current_shape.shape[1]):
                if self.current_shape[r, c]:
                    self.board[row + r, col + c] = 1
        self.current_shape = None
        self._clear_rows()

    def _clear_rows(self):
        """
        Clear full rows on the board.
        """
        full_rows = [r for r in range(self.rows) if all(self.board[r])]
        for row in full_rows:
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
                        temp_board[row + r, col + c] = 1
        print(temp_board, end='\n\n')



def main():

    shape = np.array([[1, 1, 0],
                      [0, 1, 1],
                      [0, 0, 0]])

    # Create the Tetris table
    tetris = Table()

    # Spawn the shape
    tetris.spawn_shape(shape)

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

if __name__ == '__main__':
    main()


