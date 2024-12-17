import pygame
import random
import sys
from Definitions import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, BOARD_WIDTH, BOARD_HEIGHT, PLAY_WITH_AI, FPS
from Table import Table

# Timer
def initialize_timer_and_score():
    return pygame.time.get_ticks(), 0

def update_timer(start_time):
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) // 1000
    return elapsed_time

#  Scoring System - visual basic thing
def draw_timer_and_score(screen, elapsed_time, score, x_offset=0):
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Time: {elapsed_time}s", True, (255, 255, 255))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(timer_text, (10 + x_offset, 10))
    screen.blit(score_text, (10 + x_offset, 50))

# Abstract Interface for Players
def handle_human_input(keys, table):
    if keys[pygame.K_LEFT]:
        table.shift_left()
    if keys[pygame.K_RIGHT]:
        table.shift_right()
    if keys[pygame.K_DOWN]:
        table.drop()
    if keys[pygame.K_UP]:
        table.rotate()

# Main Game Loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Initialize tables
    human_table = Table(BOARD_HEIGHT, BOARD_WIDTH)
    ai_table = Table(BOARD_HEIGHT, BOARD_WIDTH) if PLAY_WITH_AI else None

    # Initialize scoring and timer
    start_time, human_score = initialize_timer_and_score()
    ai_score = 0 if PLAY_WITH_AI else None

    # Spawn initial shapes
    human_table.spawn_shape(random.choice(list(Table._shapes.values())))
    if ai_table:
        ai_table.spawn_shape(random.choice(list(Table._shapes.values())))

    running = True

     # game loop
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle input for human player
        keys = pygame.key.get_pressed()
        handle_human_input(keys, human_table)

        # Update AI player if enabled
        if PLAY_WITH_AI and ai_table:
            # TODO: bulid AI player logic
            ai_table.drop()

        # Update timers and scores
        elapsed_time = update_timer(start_time)
        human_score += 1  # Placeholder; TODO: bulid scoring based on gameplay events
        if PLAY_WITH_AI:
            ai_score += 1  # TODO: bulid scoring for AI score logic

        # Draw everything
        screen.fill((0, 0, 0))

        # Draw human table
        human_table.display_board()
        draw_timer_and_score(screen, elapsed_time, human_score)

        # Draw AI table if enabled
        if PLAY_WITH_AI and ai_table:
            ai_table.display_board()
            draw_timer_and_score(screen, elapsed_time, ai_score, x_offset=SCREEN_WIDTH // 2)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
