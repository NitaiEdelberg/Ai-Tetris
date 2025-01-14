import pygame
from Gameplay import Definitions

def draw_grid(screen, x_offset=0):
    """
    Draw the grid lines on the screen with an optional horizontal offset.
    :param screen: Pygame screen surface.
    :param x_offset: Horizontal offset for drawing the grid.
    """
    for x in range(0, Definitions.SCREEN_WIDTH, Definitions.GRID_SIZE):
        pygame.draw.line(screen, Definitions.WHITE, (x + x_offset, 0), (x + x_offset, Definitions.SCREEN_HEIGHT))
    for y in range(0, Definitions.SCREEN_HEIGHT, Definitions.GRID_SIZE):
        pygame.draw.line(screen, Definitions.WHITE, (x_offset, y), (Definitions.SCREEN_WIDTH + x_offset, y))

def draw_board(screen, board, shape=None, shape_name=None, position=(0, 0), x_offset=0):
    """
    Draw the board and the current shape on the screen.

    :param screen: Pygame screen surface.
    :param board: Current state of the Tetris board.
    :param shape: Current shape being controlled (optional).
    :param shape_name: Current shape name (optional).
    :param position: Tuple (row, col) for the top-left position of the shape.
    :param x_offset: Horizontal offset for drawing the board.
    """
    for row in range(board.shape[0]):
        for col in range(board.shape[1]):
            if board[row, col] > 0:
                pygame.draw.rect(
                    screen,
                    Definitions.COLOR_SHAPES[board[row, col]],
                    pygame.Rect(
                        col * Definitions.GRID_SIZE + x_offset,
                        row * Definitions.GRID_SIZE,
                        Definitions.GRID_SIZE,
                        Definitions.GRID_SIZE
                    )
                )
                pygame.draw.rect(
                    screen,
                    Definitions.WHITE,
                    pygame.Rect(
                        col * Definitions.GRID_SIZE + x_offset,
                        row * Definitions.GRID_SIZE,
                        Definitions.GRID_SIZE,
                        Definitions.GRID_SIZE
                    ),
                    1
                )

    if shape_name is not None and shape is not None:
        shape_row, shape_col = position
        for r in range(shape.shape[0]):
            for c in range(shape.shape[1]):
                if shape[r, c]:
                    pygame.draw.rect(
                        screen,
                        Definitions.SHAPES_COLORS.get(shape_name),
                        pygame.Rect(
                            (shape_col + c) * Definitions.GRID_SIZE + x_offset,
                            (shape_row + r) * Definitions.GRID_SIZE,
                            Definitions.GRID_SIZE,
                            Definitions.GRID_SIZE
                        )
                    )
                    pygame.draw.rect(
                        screen,
                        Definitions.WHITE,
                        pygame.Rect(
                            (shape_col + c) * Definitions.GRID_SIZE + x_offset,
                            (shape_row + r) * Definitions.GRID_SIZE,
                            Definitions.GRID_SIZE,
                            Definitions.GRID_SIZE
                        ),
                        1
                    )

def draw_timer_and_score(screen, elapsed_time, score, x_offset=0):
    """
    Draw the timer and score on the screen.
    :param screen: Pygame screen surface.
    :param elapsed_time: Time elapsed since the start of the game.
    :param score: Current score.
    :param x_offset: Horizontal offset for the text display.
    """
    font = pygame.font.Font(None, Definitions.FONT_SIZE)
    timer_text = font.render(f"Time: {elapsed_time}s", True, Definitions.WHITE)
    score_text = font.render(f"Score: {score}", True, Definitions.WHITE)

    screen.blit(timer_text, (Definitions.TIMER_POS[0] + x_offset, Definitions.TIMER_POS[1]))
    screen.blit(score_text, (Definitions.SCORE_POS[0] + x_offset, Definitions.SCORE_POS[1]))

def draw_game_over(screen, final_score, elapsed_time, x_offset=0):
    """
    Display the "Game Over" screen with the final score and elapsed time for a specific player.
    :param screen: Pygame screen surface.
    :param final_score: The final score of the player.
    :param elapsed_time: The total elapsed time in seconds.
    :param x_offset: Horizontal offset for the player's game over screen.
    """
    font = pygame.font.Font(None, Definitions.FONT_SIZE * 2)  # Larger font for "Game Over"
    small_font = pygame.font.Font(None, Definitions.FONT_SIZE)
    tiny_font = pygame.font.Font(None, Definitions.FONT_SIZE // 2)

    # Render the "Game Over" text
    game_over_text = font.render("Game Over", True, Definitions.RED)
    game_over_rect = game_over_text.get_rect(center = (Definitions.SCREEN_WIDTH // 2 + x_offset, Definitions.SCREEN_HEIGHT // 3))
    screen.blit(game_over_text, game_over_rect)

    # Render the final score
    score_text = small_font.render(f"Final Score: {final_score}", True, Definitions.PINK)
    score_rect = score_text.get_rect(center =(Definitions.SCREEN_WIDTH // 2 + x_offset, Definitions.SCREEN_HEIGHT // 2))
    screen.blit(score_text, score_rect)

    # Render the total elapsed time
    time_text = small_font.render(f"Time Played: {elapsed_time}s", True, Definitions.PINK)
    time_rect = time_text.get_rect(center = (Definitions.SCREEN_WIDTH // 2 + x_offset, Definitions.SCREEN_HEIGHT // 2 + 50))
    screen.blit(time_text, time_rect)

    # Render the "Press 'Q' to quit" message
    quit_text = tiny_font.render("Press 'Q' to quit", True, Definitions.PINK)
    quit_rect = quit_text.get_rect(center = (Definitions.SCREEN_WIDTH // 2 + x_offset, Definitions.SCREEN_HEIGHT - 30))
    screen.blit(quit_text, quit_rect)

    pygame.display.flip()
