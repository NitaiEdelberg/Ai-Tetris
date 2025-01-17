# Game Definitions
from turtledemo.nim import COLOR

import numpy as np
GRID_SIZE = 32 # Size of the screen
BOARD_WIDTH, BOARD_HEIGHT = 10, 20 # Size of the board
SCREEN_WIDTH, SCREEN_HEIGHT = GRID_SIZE * BOARD_WIDTH, GRID_SIZE * BOARD_HEIGHT
DROP_INTERVAL = 500  # Time in milliseconds between automatic drops
FPS = 50 #frames per seconds
PLAY_WITH_AI = True
PLAY_WITH_HUMAN = True
GRAPHICS_ON = True
AI_PLAY_WITH_GRAPHIC = True
PROCESS_NUM = 10

# Colors (RGB)
WHITE = (255, 255, 255)
CYAN = (1, 237, 250)
NAVY = (46, 46, 132)
ORANGE = (220, 88, 42)
YELLOW = (254,221,0)
GREEN = (83, 218, 63)
PURPLE = (221, 10, 178)
RED = (234, 20, 28)
PINK = (255,51,255)

# Shapes
SHAPES = {
        'I': np.array([
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]),
        'J': np.array([
            [2, 0, 0],
            [2, 2, 2],
            [0, 0, 0],
        ]),
        'L': np.array([
            [0, 0, 3],
            [3, 3, 3],
            [0, 0, 0],
        ]),
        'O': np.array([
            [4, 4],
            [4, 4],
        ]),
        'S': np.array([
            [0, 5, 5],
            [5, 5, 0],
            [0, 0, 0],
        ]),
        'Z': np.array([
            [6, 6, 0],
            [0, 6, 6],
            [0, 0, 0],
        ]),
        'T': np.array([
            [0, 7, 0],
            [7, 7, 7],
            [0, 0, 0],
        ])
    }

SHAPES_COLORS = {
        'I': CYAN,
        'J': NAVY,
        'L': ORANGE,
        'O': YELLOW,
        'S': GREEN,
        'Z': RED,
        'T': PURPLE
    }

COLOR_SHAPES = [PINK,CYAN,NAVY,ORANGE,YELLOW,GREEN,RED,PURPLE]


# Display design



# Font size
FONT_SIZE = 36

# Text positions
TIMER_POS = (10, 10)  # x=10, y=10
SCORE_POS = (10, 50)  # x=10, y=50
GAME_OVER_POS = (100, 100)

# Offset for horizontal adjustment
DEFAULT_X_OFFSET = 0

# Points
POINTS_PER_LINE = [0,40, 100, 300, 1200]  #[NONE,SINGLE, DOUBLE, TRIPLE, TETRIS]
