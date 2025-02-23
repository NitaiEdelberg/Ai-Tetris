import pygame
from Gameplay.Table import Table
from Gameplay import Definitions

class HumanHandler:
    """
    Class to handle the human player's game logic and inputs.
    """
    def __init__(self):
        self.table = Table(Definitions.BOARD_HEIGHT, Definitions.BOARD_WIDTH)
        self.score = 0
        self.last_drop_time = pygame.time.get_ticks()
        self.active = True
        self.end_time = None
        self.table.spawn_next_shape()

    def handle_input(self):
        """Handles human player's key inputs."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.table.shift_left()
        elif keys[pygame.K_RIGHT]:
            self.table.shift_right()
        elif keys[pygame.K_DOWN]:
            self.table.drop()
        elif keys[pygame.K_UP]:
            self.table.rotate()

    def update(self, elapsed_time):
        """Updates the human player's game state."""
        if not self.active:
            return

        self.handle_input()
        current_time = pygame.time.get_ticks()
        if current_time - self.last_drop_time > Definitions.DROP_INTERVAL:
            if not self.table.is_shape_landing():
                self.table.drop()
            else:
                lines_cleaned = self.table.check_for_cleared_rows()
                if lines_cleaned > 0:
                    self.score += Definitions.POINTS_PER_LINE[lines_cleaned]
                self.table.spawn_next_shape()
            self.last_drop_time = current_time

        if self.table.game_over:
            self.active = False
            self.end_time = elapsed_time
