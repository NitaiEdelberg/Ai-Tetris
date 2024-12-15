import pygame
import sys
import Definitions
from GamePlay.Table import Table
import time

# Initialize pygame and constants
pygame.init()
grid_size = Definitions.GRID_SIZE
screen_width, screen_height = Definitions.SCREEN_WIDTH, Definitions.SCREEN_HEIGHT
prize_for_clean = Definitions.PRIZE_FOR_CLEAN
fps = Definitions.FPS

# Colors
BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)

class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize game components
        self.table = Table(Definitions.BOARD_HEIGHT, Definitions.BOARD_WIDTH)
        self.score = 0
        self.start_time = time.time()

    def handle_player_input(self):
        """
        Handle player input for movement and rotation.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.table.shift_left()
        if keys[pygame.K_RIGHT]:
            self.table.shift_right()
        if keys[pygame.K_DOWN]:
            self.table.drop()
        if keys[pygame.K_UP]:
            self.table.rotate()

    def update_score(self, rows_cleared):
        """
        Update the score based on the number of rows cleared.
        """
        self.score += rows_cleared * prize_for_clean

    def display_game(self):
        """
        Render the game board, score, and timer.
        """
        self.screen.fill(BACKGROUND_COLOR)

        # Draw the game board
        self.table.display_board()

        # Display score and timer
        elapsed_time = int(time.time() - self.start_time)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, TEXT_COLOR)
        timer_text = font.render(f"Time: {elapsed_time}s", True, TEXT_COLOR)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(timer_text, (10, 50))

        pygame.display.flip()

    def game_loop(self):
        """
        Main game loop.
        """
        while self.running:
            self.clock.tick(fps)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Handle input and game logic
            self.handle_player_input()
            self.table.drop()

            # Check for cleared rows
            cleared_rows = self.table._clear_rows()  # Returns number of cleared rows
            self.update_score(cleared_rows)

            # display the game
            self.display_game()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = TetrisGame()
    game.game_loop()
