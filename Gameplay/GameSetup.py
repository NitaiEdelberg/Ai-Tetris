import multiprocessing
# import pygame
import sys
import time

from scipy.fft import ifft2

from AIPlayer.AIAgent import AIAgent
from Gameplay.Table import Table
from Gameplay import Display
from Gameplay import Definitions

# Timer
def initialize_timer():
    return pygame.time.get_ticks()

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

def run_tetris_game(ai_agent: AIAgent) -> int:
    """
    Run a Tetris game with AI only.

    Parameters:
    - ai_agent (AIAgent): The AI agent controlling the game.

    Returns:
    - int: AI score.
    """
    ai_end_time = None

    # Initialize Table Instance for AI
    ai_table = Table(Definitions.BOARD_HEIGHT, Definitions.BOARD_WIDTH)

    # Initialize scoring and timer
    start_time = time.time()
    ai_score = 0

    # Spawn initial shape
    ai_table.spawn_next_shape()

    running = True

    # Game loop
    while running:
        current_time = time.time()

        # AI logic
        ai_agent.choose_action(ai_table)

        if ai_table.is_shape_landing():
            lines_cleaned = ai_table.check_for_cleared_rows()
            if lines_cleaned > 0:
                ai_score += Definitions.POINTS_PER_LINE[lines_cleaned]
            ai_table.spawn_next_shape()

        # Check game over for AI
        if ai_table.game_over:
            running = False
            ai_end_time = int(current_time - start_time)
            print(f"AI Score: {ai_score}, Time: {ai_end_time}")

    return ai_score

def run_tetris_game_with_graphics(play_with_human : bool = False, ai_agent : AIAgent = None) -> int:
    human_end_time = None
    ai_end_time = None

    pygame.init()
    screen_width = Definitions.SCREEN_WIDTH * 2 if AIAgent and play_with_human else Definitions.SCREEN_WIDTH
    screen = pygame.display.set_mode((screen_width, Definitions.SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Initialize Table Instances
    human_table = Table(Definitions.BOARD_HEIGHT, Definitions.BOARD_WIDTH) if play_with_human else None
    ai_table = Table(Definitions.BOARD_HEIGHT, Definitions.BOARD_WIDTH) if AIAgent else None

    # Initialize scoring and timer
    start_time = initialize_timer()
    human_score = 0 if play_with_human else None
    ai_score = 0 if AIAgent else None

    # Spawn initial shapes
    if human_table:
        human_table.spawn_next_shape()
    if ai_table:
        ai_table.spawn_next_shape()

    human_last_drop_time = pygame.time.get_ticks() if human_table else None
    ai_last_drop_time = pygame.time.get_ticks() if ai_table else None

    running = True
    human_active = True if play_with_human else False
    ai_active = True if AIAgent else False

    # Game Loop
    while running:
        clock.tick(Definitions.FPS)

        #******************************** human ***********************************
        # Event handling
        if play_with_human:
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
                    human_score += Definitions.POINTS_PER_LINE[lines_cleaned]
                human_table.spawn_next_shape()
            human_last_drop_time = current_time

        # ************************************ AI *************************************************
        # Update AI player
        if ai_table and ai_active and Definitions.PLAY_WITH_AI:
            ai_agent.choose_action(ai_table)
            # if current_time - ai_last_drop_time > Definitions.DROP_INTERVAL:
            #     if not ai_table.is_shape_landing():
            #         #ai_table.drop()
            #         continue
            #     else:
            #         lines_cleaned = ai_table.check_for_cleared_rows()
            #         if lines_cleaned > 0:
            #             ai_score += Definitions.POINTS_PER_LINE[lines_cleaned]
            #         ai_table.spawn_next_shape()
            #     ai_last_drop_time = current_time
            if ai_table.is_shape_landing():
                lines_cleaned = ai_table.check_for_cleared_rows()
                if lines_cleaned > 0:
                    ai_score += Definitions.POINTS_PER_LINE[lines_cleaned]
                ai_table.spawn_next_shape()

        # Update timers and scores
        elapsed_time = update_timer(start_time)

        # Check game over for human
        if human_table and human_active and human_table.game_over:
            human_active = False
            human_end_time = elapsed_time

        # Check game over for AI
        if ai_table and ai_active and ai_table.game_over:
            ai_active = False
            ai_end_time = elapsed_time

        # End game if both players are inactive
        if not human_active and not ai_active:
            running = False

        # Draw everything
        if Definitions.GRAPHICS_ON:
            screen.fill((0, 0, 0))
            Display.draw_grid(screen, 0)

            if human_table:
                Display.draw_board(screen, human_table.board, human_table.current_shape, human_table.current_shape_name,
                                   human_table.shape_position, x_offset=0)
                if human_active:
                    Display.draw_timer_and_score(screen, elapsed_time, human_score, 0)
                else:
                    Display.draw_timer_and_score(screen, human_end_time, human_score, 0)
                if not human_active:
                    Display.draw_game_over(screen, human_score, human_end_time, 0)

            if ai_table and Definitions.AI_PLAY_WITH_GRAPHIC:
                Display.draw_grid(screen, Definitions.SCREEN_WIDTH)
                Display.draw_board(screen, ai_table.board, ai_table.current_shape, ai_table.current_shape_name,
                                   ai_table.shape_position, x_offset=Definitions.SCREEN_WIDTH) if play_with_human and AIAgent else Display.draw_board(screen, ai_table.board, ai_table.current_shape, ai_table.current_shape_name,
                                   ai_table.shape_position, x_offset=0)
                if ai_active:
                    Display.draw_timer_and_score(screen, elapsed_time, ai_score, Definitions.SCREEN_WIDTH) if play_with_human and AIAgent else Display.draw_timer_and_score(screen, elapsed_time, ai_score, 0)
                else:
                    Display.draw_timer_and_score(screen, ai_end_time, ai_score, Definitions.SCREEN_WIDTH) if play_with_human and AIAgent else Display.draw_timer_and_score(screen, ai_end_time, ai_score, 0)
                if not ai_active:
                    Display.draw_game_over(screen, ai_score, ai_end_time, Definitions.SCREEN_WIDTH) if play_with_human else Display.draw_game_over(screen, ai_score, ai_end_time, 0)

        pygame.display.flip()

    waiting = play_with_human
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                waiting = False
    pygame.quit()
    if AIAgent:
        return ai_score
    else:
        return human_score

# Main Game Loop
def main():
    # ai_agent_optimal = AIAgent(-0.42311679935207946, -0.6050074206943761, -0.7073960737188766, 0.026416007419959753)
    # ai_agent_optimal = AIAgent(-0.2031239239304267, -0.9012882787168671, -0.36325534782999528, 0.873019662877332)
    ai_agent_optimal = AIAgent(-0.16044284177187973, -0.0029765700302580283, -0.8278209387332695, 0.06613546738395593)
    # ai_agent_optimal = AIAgent(-0.41503952099193375, -0.9789465866960196, -0.8851436530882919, 0.43928167880791913)
    # ai_agent_optimal_2 = AIAgent(-0.184483, -0.510066, -0.35663, 0.760666)
    print(run_tetris_game_with_graphics(ai_agent=ai_agent_optimal))
    # print(run_tetris_game_with_graphics(ai_agent=ai_agent_optimal_2))
    # run_tetris_game_with_graphics(play_with_human=True, ai_agent=ai_agent_optimal)
    sys.exit()


if __name__ == "__main__":
    main()
