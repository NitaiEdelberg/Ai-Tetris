import pygame
import random
import sys
import Definitions
from Table import Table
import Display

# Timer
def initialize_timer_and_score():
    return pygame.time.get_ticks(), 0

def update_timer(start_time):
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) // 1000
    return elapsed_time

"""
 Abstract Interface for Human Players

 :param keys: which key is pressed. 
 :param table: The table class.
 """
def handle_human_input(keys, table):
    if keys[pygame.K_LEFT]:
        table.shift_left()
    elif keys[pygame.K_RIGHT]:
        table.shift_right()
    elif keys[pygame.K_DOWN]:
        table.drop()
    elif keys[pygame.K_UP]:
        table.rotate()

# Main Game Loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((Definitions.SCREEN_WIDTH, Definitions.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    """
    Initialize Human table Instance and AI if needed.

    :param rows: Number of rows on the board.
    :param cols: Number of columns on the board.
    """

    human_table = Table(Definitions.BOARD_HEIGHT, Definitions.BOARD_WIDTH)
    ai_table = Table(Definitions.BOARD_HEIGHT, Definitions.BOARD_WIDTH) if Definitions.PLAY_WITH_AI else None

    """
    Initialize scoring and timer
    """
    start_time, human_score = initialize_timer_and_score()
    ai_score = 0 if Definitions.PLAY_WITH_AI else None

    """
    Spawn initial shapes
    """
    human_table.spawn_next_shape()
    if ai_table:
        ai_table.spawn_next_shape()

    """
    Initialize drop timers
    """
    human_last_drop_time = pygame.time.get_ticks()
    ai_last_drop_time = pygame.time.get_ticks() if Definitions.PLAY_WITH_AI else None

    running = True

    """
    Game Loop
    """
    while running:
        clock.tick(Definitions.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        """
        Automatic drop logic for human player
        """
        current_time = pygame.time.get_ticks()
        if current_time - human_last_drop_time > Definitions.DROP_INTERVAL:
            if not human_table.is_shape_landing():  # If shape hasn't landed yet, drop it
                human_table.drop()
            else:
                # Check for full line and update score
                if human_table.check_for_full_line():
                    human_score += Definitions.PRIZE_FOR_CLEAN

                human_table.spawn_next_shape()  # Spawn a new shape

        human_last_drop_time = current_time  # Reset drop timer

        # Handle input for human player
        keys = pygame.key.get_pressed()
        handle_human_input(keys, human_table)

        # Update AI player if enabled
        if Definitions.PLAY_WITH_AI and ai_table:
            if current_time - ai_last_drop_time > Definitions.DROP_INTERVAL:
                if not ai_table.is_shape_landing():  # If shape hasn't landed yet, drop it
                    ai_table.drop()
                else:
                    # Check for full line and update AI score
                    if ai_table.check_for_cleared_rows() > 0:
                        ai_score += Definitions.PRIZE_FOR_CLEAN
                    ai_table.spawn_next_shape()  # Spawn a new shape
                ai_last_drop_time = current_time  # Reset AI drop timer


        # Update timers and scores
        elapsed_time = update_timer(start_time)

        # Draw everything
        screen.fill((0, 0, 0))

        # Draw human table
        human_table.display_board()
        Display.draw_timer_and_score(screen, elapsed_time, human_score)

        # Draw AI table if enabled
        if Definitions.PLAY_WITH_AI and ai_table:
            ai_table.display_board()
            Display.draw_timer_and_score(screen, elapsed_time, ai_score, x_offset=Definitions.SCREEN_WIDTH // 2)

        pygame.display.flip()


    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()