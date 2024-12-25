import pygame
import sys
import Definitions
from AIPlayer.AIAgent import AIAgent
from Table import Table
import Display

# Timer
def initialize_timer_and_score():
    return pygame.time.get_ticks(), 0

def update_timer(start_time):
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) // 1000
    return elapsed_time

# Handle human input
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
    human_end_time = None
    ai_end_time = None
    pygame.init()
    screen_width = Definitions.SCREEN_WIDTH * 2 if Definitions.PLAY_WITH_AI else Definitions.SCREEN_WIDTH
    screen = pygame.display.set_mode((screen_width, Definitions.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Initialize Table Instances
    human_table = Table(Definitions.BOARD_HEIGHT, Definitions.BOARD_WIDTH) if Definitions.PLAY_WITH_HUMAN else None
    ai_table = Table(Definitions.BOARD_HEIGHT, Definitions.BOARD_WIDTH) if Definitions.PLAY_WITH_AI else None

    # Initialize AI agent
    ai_agent = AIAgent() if Definitions.PLAY_WITH_AI else None

    # Initialize scoring and timer
    start_time, human_score = initialize_timer_and_score()
    ai_score = 0 if Definitions.PLAY_WITH_AI else None

    # Spawn initial shapes
    if human_table:
        human_table.spawn_next_shape()
    if ai_table:
        ai_table.spawn_next_shape()

    human_last_drop_time = pygame.time.get_ticks() if human_table else None
    ai_last_drop_time = pygame.time.get_ticks() if ai_table else None

    running = True
    human_active = True
    ai_active = True

    # Game Loop
    while running:
        clock.tick(Definitions.FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if human_table and human_active and event.type == pygame.KEYDOWN:
                handle_human_input(pygame.key.get_pressed(), human_table)

        # Handle continuous input for human
        if human_table and human_active:
            keys = pygame.key.get_pressed()
            handle_human_input(keys, human_table)

        # Automatic drop logic for human player
        current_time = pygame.time.get_ticks()
        if human_table and human_active and current_time - human_last_drop_time > Definitions.DROP_INTERVAL:
            if not human_table.is_shape_landing():
                human_table.drop()
            else:
                lines_cleaned = human_table.check_for_cleared_rows()
                if lines_cleaned > 0:
                    human_score += Definitions.POINTS_PER_LINE[lines_cleaned - 1]
                human_table.spawn_next_shape()

            human_last_drop_time = current_time

        # Update AI player
        if ai_table and ai_active and Definitions.PLAY_WITH_AI:
            ai_agent.choose_action(ai_table)
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
        if Definitions.GRAPHICS_ON:
            screen.fill((0, 0, 0))
            Display.draw_grid(screen, 0)

            if human_table:
                Display.draw_board(screen, human_table.board, human_table.current_shape, human_table.current_shape_name, human_table.shape_position, x_offset=0)
                if human_active:
                    Display.draw_timer_and_score(screen, elapsed_time, human_score, 0)
                else:
                    Display.draw_timer_and_score(screen, human_end_time, human_score, 0)
                if not human_active:
                    Display.draw_game_over(screen, human_score, human_end_time, 0)

            if ai_table and Definitions.AI_PLAY_WITH_GRAPHIC:
                Display.draw_grid(screen, Definitions.SCREEN_WIDTH)
                Display.draw_board(screen, ai_table.board, ai_table.current_shape, ai_table.current_shape_name, ai_table.shape_position, x_offset=Definitions.SCREEN_WIDTH)
                if ai_active:
                    Display.draw_timer_and_score(screen, elapsed_time, ai_score, Definitions.SCREEN_WIDTH)
                else:
                    Display.draw_timer_and_score(screen, ai_end_time, ai_score, Definitions.SCREEN_WIDTH)
                if not ai_active:
                    Display.draw_game_over(screen, ai_score, ai_end_time, Definitions.SCREEN_WIDTH)


        pygame.display.flip()

        # Check game over for human
        if human_table and human_active and human_table.game_over and human_active:
            human_active = False
            human_end_time = elapsed_time

        # Check game over for AI
        if ai_table and ai_active and ai_table.game_over and ai_active:
            ai_active = False
            ai_end_time = elapsed_time

        # End game if both players are inactive
        if not human_active and not ai_active:
            running = False

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                waiting = False
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
