import pygame
import Definitions

def draw_timer_and_score(screen, elapsed_time, score, x_offset=0):
    font = pygame.font.Font(None, Definitions.FONT_SIZE)
    timer_text = font.render(f"Time: {elapsed_time}s", True, Definitions.WHITE)
    score_text = font.render(f"Score: {score}", True, Definitions.WHITE)
    screen.blit(timer_text, (Definitions.TIMER_POS[0] + x_offset, Definitions.TIMER_POS[1]))
    screen.blit(score_text, (Definitions.SCORE_POS[0] + x_offset, Definitions.SCORE_POS[1]))
    screen.blit(score_text, (Definitions.SCORE_POS[0] + x_offset, Definitions.SCORE_POS[1]))