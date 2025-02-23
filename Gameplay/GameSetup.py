from multiprocessing import Process
import pygame
import sys
import os
from AIPlayer.AIAgent import AIAgent
from Gameplay import Display
from Gameplay import Definitions
from Gameplay.HumanHandler import HumanHandler
from Gameplay.AIHandler import AIHandler

def initialize_timer():
    """
    Use pygame to initialize the game timer.
    """
    return pygame.time.get_ticks()

def update_timer(start_time):
    """
    Update the timer when needed.
    """
    current_time = pygame.time.get_ticks()
    return (current_time - start_time) // 1000

def run_human_game():
    """
    Runs the Tetris game for the human player in a separate window.
    """
    os.environ['SDL_VIDEO_WINDOW_POS'] = "220,160"  # Human window starts here, next to the AI window
    pygame.init()
    screen = pygame.display.set_mode((Definitions.SCREEN_WIDTH, Definitions.SCREEN_HEIGHT)) # Set up the display window
    pygame.display.set_caption("TETRIS - HUMAN PLAYER")  # Window title
    clock = pygame.time.Clock() # Create a clock object to control the frame rate

    human = HumanHandler() # Create an instance of the HumanHandler class to manage the human player's actions
    start_time = initialize_timer()
    running = True

    while running:
        clock.tick(Definitions.HUMAN_FPS) # Control the game loop to run at the specified FPS
        # Check for user input (quit event or pressed 'Q' key for quiting)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                running = False

        elapsed_time = update_timer(start_time) # Calculate the elapsed time since the game started
        human.update(elapsed_time)
        screen.fill((0, 0, 0)) # Clear the screen and fill it with a black background
        Display.draw_grid(screen, 0) # Draw the game grid
        # Draw the current game board and the shapes on the screen
        Display.draw_board(screen, human.table.board, human.table.current_shape, human.table.current_shape_name,
                           human.table.shape_position, x_offset=0)
        # Draw the human timer and score on the screen
        Display.draw_timer_and_score(screen, elapsed_time if human.active else human.end_time, human.score, 0)

        if not human.active: # If the game is over, display the game over screen
            Display.draw_game_over(screen, human.score, human.end_time, 0)

        pygame.display.flip() # Update the display with the new content

    pygame.quit() # Quit pygame when the game loop ends


def run_ai_game(ai_agent):
    """
    Runs the Tetris game for the AI player in a separate window.
    """
    pygame.init()
    screen = pygame.display.set_mode((Definitions.SCREEN_WIDTH, Definitions.SCREEN_HEIGHT))  # Set up the display window
    pygame.display.set_caption("TETRIS - AI PLAYER")  # Window title
    clock = pygame.time.Clock() # Create a clock object

    ai = AIHandler(ai_agent) # Create an instance of the AIHandler class to manage the AI player's actions
    start_time = initialize_timer()
    running = True

    while running:
        clock.tick(Definitions.AI_FPS) # Control the game loop to run at the specified FPS

        for event in pygame.event.get():  # Check for user input (quit event)
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                running = False

        elapsed_time = update_timer(start_time) # Calculate the elapsed time since the game started
        ai.update(elapsed_time) # Update the AI player's state based on elapsed time
        screen.fill((0, 0, 0)) # Clear the screen and fill it with a black background
        Display.draw_grid(screen, 0) # Draw the game grid
        # Draw the current game board and the shapes on the screen
        Display.draw_board(screen, ai.table.board, ai.table.current_shape, ai.table.current_shape_name,
                           ai.table.shape_position, x_offset=0)
        # Draw the timer and score on the screen
        Display.draw_timer_and_score(screen, elapsed_time if ai.active else ai.end_time, ai.score, 0)

        if not ai.active: # If the game is over, display the game over screen
            Display.draw_game_over(screen, ai.score, ai.end_time, 0)

        pygame.display.flip() # Update the display with the new content

    pygame.quit() # Quit pygame when the game loop ends


def main():
    """
    Starts the human and AI games in separate processes based on user input.
    """
    # Ask the user if they want to play
    human_choice = input("Do you want to play? Press Y for yes and N for no: ").strip().upper()

    # Ask the user if they want the AI to play
    ai_choice = input("Do you want the AI to play? Press Y for yes and N for no: ").strip().upper()

    if (human_choice != ('Y' or 'y')) and (ai_choice != ('Y' or 'y')):
        print("Invalid input. Exiting game...")
        return  # Exit if the input is invalid

    print("starting the game..............")

    if human_choice == ('Y' or 'y'):
        human_process = Process(target=run_human_game)
        human_process.start()

    if ai_choice == ('Y' or 'y'):
        ai_agent_optimal = AIAgent(-0.147593415829753, -0.16684726563044971, -0.7783947049391171, 0.03811992593777204)
        ai_process = Process(target=run_ai_game, args=(ai_agent_optimal,))
        ai_process.start()

    if human_choice == ('Y' or 'y'): human_process.join()
    if ai_choice == ('Y' or 'y'): ai_process.join()

    sys.exit()



if __name__ == "__main__":
    main()
