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
Abstract Interface for Human Players.

:param keys: The key that was pressed
:param table: A table Object (could be unman or ai)
:void: activate an action from the Table class
 
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

    # Initaialize Table Instance
    human_table = Table(Definitions.BOARD_HEIGHT, Definitions.BOARD_WIDTH)
    ai_table = Table(Definitions.BOARD_HEIGHT, Definitions.BOARD_WIDTH) if Definitions.PLAY_WITH_AI else None

    # Initialize scoring and timer
    start_time, human_score = initialize_timer_and_score()
    ai_score = 0 if Definitions.PLAY_WITH_AI else None

    # Spawn initial shapes
    human_table.spawn_next_shape()
    if ai_table:
        ai_table.spawn_next_shape()

    human_last_drop_time = pygame.time.get_ticks()
    ai_last_drop_time = pygame.time.get_ticks() if Definitions.PLAY_WITH_AI else None

    running = True

    #Game Loop while running:
    while running:
        clock.tick(Definitions.FPS)

        # Event handling
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # Rotate shape
                    human_table.rotate()
                elif event.key == pygame.K_DOWN:  # Immediate drop
                    human_table.drop()

        # Continuous movement with key holding to enable moving 'speed'.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            human_table.shift_left()
        elif keys[pygame.K_RIGHT]:
            human_table.shift_right()
        elif(keys[pygame.K_DOWN]):
            human_table.drop()


        # Automatic drop logic for human player
        current_time = pygame.time.get_ticks()
        if current_time - human_last_drop_time > Definitions.DROP_INTERVAL:
            if not human_table.is_shape_landing():
                human_table.drop()
            # if shape landed, check for row complitment and spawn the next shape
            else:
                lines_cleaned = human_table.check_for_cleared_rows()
                if lines_cleaned > 0:
                    human_score += Definitions.POINTS_PER_LINE[lines_cleaned - 1]
                human_table.spawn_next_shape()

            human_last_drop_time = current_time

        # Update AI player if enabled
        if Definitions.PLAY_WITH_AI and ai_table:
            if current_time - ai_last_drop_time > Definitions.DROP_INTERVAL:
                if not ai_table.is_shape_landing():
                    ai_table.drop()
                else:
                    lines_cleaned = ai_table.check_for_cleared_rows()
                    if lines_cleaned > 0:
                        ai_score += Definitions.POINTS_PER_LINE[lines_cleaned - 1]
                    ai_table.spawn_next_shape()
                ai_last_drop_time = current_time

        # Update timers and scores
        elapsed_time = update_timer(start_time)

        # Draw everything
        screen.fill((0, 0, 0))
        Display.draw_grid(screen)
        Display.draw_board(screen, human_table.board,human_table.current_shape, human_table.current_shape_name, human_table.shape_position)
        Display.draw_timer_and_score(screen, elapsed_time, human_score)

        if Definitions.PLAY_WITH_AI and ai_table:
            # for ai player use default console to avoid time loos by rendering graphic.
            ai_table.display_board()
            Display.draw_timer_and_score(screen, elapsed_time, ai_score, x_offset=Definitions.SCREEN_WIDTH // 2)

        pygame.display.flip()

        if human_table.game_over:
            screen.fill((0, 0, 0))
            Display.draw_game_over(screen,human_score,elapsed_time)
            # Wait for a 'q' key press to quit the game
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        running = False

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            waiting = False
                            running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


