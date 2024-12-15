import pygame
import random
import sys
import Definitions

# Constants
grid_size = Definitions.GRID_SIZE
borad_width, board_height = Definitions.BOARD_WIDTH, Definitions.BOARD_HEIGHT
screen_width, screen_height = Definitions.SCREEN_WIDTH, Definitions.SCREEN_HEIGHT

# Initialize playfield
def initialize_playfield():
    return [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

# Rotate a matrix 90 degrees clockwise
def rotate(matrix):
    return [list(row) for row in zip(*matrix[::-1])]

# Generate a sequence of tetromino pieces
def generate_sequence():
    sequence = list(_Shapes.keys())
    random.shuffle(sequence)
    return sequence

# Check if a move is valid
def is_valid_move(matrix, field, row, col):
    for r, row_data in enumerate(matrix):
        for c, cell in enumerate(row_data):
            if cell:
                if (
                    col + c < 0 or col + c >= BOARD_WIDTH or
                    row + r >= BOARD_HEIGHT or
                    field[row + r][col + c]
                ):
                    return False
    return True

# Place the tetromino on the playfield
def place_tetromino(field, tetromino):
    for r, row_data in enumerate(tetromino['matrix']):
        for c, cell in enumerate(row_data):
            if cell:
                field[tetromino['row'] + r][tetromino['col'] + c] = tetromino['name']

# Clear completed lines
def clear_lines(field):
    cleared_rows = 0
    new_field = [row for row in field if any(cell == 0 for cell in row)]
    cleared_rows = BOARD_HEIGHT - len(new_field)
    new_field = [[0] * BOARD_WIDTH for _ in range(cleared_rows)] + new_field
    return new_field, cleared_rows

# Draw the playfield and tetromino
def draw_field(screen, field, tetromino):
    screen.fill((0, 0, 0))  # Clear screen

    # Draw playfield
    for r, row in enumerate(field):
        for c, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, COLORS[cell],
                                 (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

    # Draw active tetromino
    for r, row in enumerate(tetromino['matrix']):
        for c, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, COLORS[tetromino['name']],
                                 ((tetromino['col'] + c) * GRID_SIZE,
                                  (tetromino['row'] + r) * GRID_SIZE,
                                  GRID_SIZE - 1, GRID_SIZE - 1))

    pygame.display.flip()

# Main game loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    playfield = initialize_playfield()
    sequence = generate_sequence()
    tetromino = {'name': sequence.pop(), 'matrix': _Shapes[sequence[-1]], 'row': -2, 'col': BOARD_WIDTH // 2 - 2}
    drop_timer = 0

    running = True
    while running:
        clock.tick(60)  # 60 FPS
        drop_timer += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle tetromino movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and is_valid_move(tetromino['matrix'], playfield, tetromino['row'], tetromino['col'] - 1):
            tetromino['col'] -= 1
        if keys[pygame.K_RIGHT] and is_valid_move(tetromino['matrix'], playfield, tetromino['row'], tetromino['col'] + 1):
            tetromino['col'] += 1
        if keys[pygame.K_DOWN] and is_valid_move(tetromino['matrix'], playfield, tetromino['row'] + 1, tetromino['col']):
            tetromino['row'] += 1
        if keys[pygame.K_UP]:
            rotated = rotate(tetromino['matrix'])
            if is_valid_move(rotated, playfield, tetromino['row'], tetromino['col']):
                tetromino['matrix'] = rotated

        # Drop tetromino every 30 frames
        if drop_timer >= 30:
            drop_timer = 0
            if is_valid_move(tetromino['matrix'], playfield, tetromino['row'] + 1, tetromino['col']):
                tetromino['row'] += 1
            else:
                place_tetromino(playfield, tetromino)
                playfield, _ = clear_lines(playfield)
                if not sequence:
                    sequence = generate_sequence()
                tetromino = {'name': sequence.pop(), 'matrix': _Shapes[sequence[-1]], 'row': -2, 'col': BOARD_WIDTH // 2 - 2}

        draw_field(screen, playfield, tetromino)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()