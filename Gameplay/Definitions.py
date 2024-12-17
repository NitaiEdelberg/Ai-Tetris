# Game Definitions
import numpy as np
GRID_SIZE = 32 # Size of the screen
BOARD_WIDTH, BOARD_HEIGHT = 10, 20 # Size of the board
SCREEN_WIDTH, SCREEN_HEIGHT = GRID_SIZE * BOARD_WIDTH, GRID_SIZE * BOARD_HEIGHT
DROP_INTERVAL = 500  # Time in milliseconds between automatic drops
PRIZE_FOR_CLEAN = 100  # Score for cleaning a full line
FPS = 1 #frames per seconds
PLAY_WITH_AI = False

# Shapes
SHAPES = {
        'I': np.array([
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]),
        'J': np.array([
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0],
        ]),
        'L': np.array([
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0],
        ]),
        'O': np.array([
            [1, 1],
            [1, 1],
        ]),
        'S': np.array([
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0],
        ]),
        'Z': np.array([
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0],
        ]),
        'T': np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0],
        ])
    }


# Display design


# Colors (RGB)
WHITE = (255, 255, 255)

# Font size
FONT_SIZE = 36

# Text positions
TIMER_POS = (10, 10)  # x=10, y=10
SCORE_POS = (10, 50)  # x=10, y=50

# Offset for horizontal adjustment
DEFAULT_X_OFFSET = 0
