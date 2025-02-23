import pygame
from AIPlayer.AIAgent import AIAgent
from Gameplay.Table import Table
from Gameplay import Definitions

class AIHandler:
    """
    Class to handle the AI player's game logic.
    """

    def __init__(self, ai_agent: AIAgent):
        self.table = Table(Definitions.BOARD_HEIGHT, Definitions.BOARD_WIDTH)
        self.ai_agent = ai_agent
        self.score = 0
        self.active = True
        self.end_time = None
        self.table.spawn_next_shape()

    def update(self, elapsed_time):
        """Updates the AI player's game state."""
        if not self.active:
            return

        self.ai_agent.choose_action(self.table)
        if self.table.is_shape_landing():
            lines_cleaned = self.table.check_for_cleared_rows()
            if lines_cleaned > 0:
                self.score += Definitions.POINTS_PER_LINE[lines_cleaned]
            self.table.spawn_next_shape()
        pygame.event.pump()

        if self.table.game_over:
            self.active = False
            self.end_time = elapsed_time
