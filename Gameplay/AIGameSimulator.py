import time

from AIPlayer import AIAgent
from Gameplay.Table import Table, Definitions


def run_tetris_game(ai_agent: AIAgent, max_placements = float('inf')) -> int:
    """
    Run a Tetris game with AI only.

    :param: ai_agent (AIAgent): The AI agent controlling the game.
    :param: max_placements (int): The maximum number of shapes to place (optional).
    :return: Final score of the game.
    """
    ai_end_time = None

    # Initialize Table Instance for AI
    ai_table = Table(Definitions.BOARD_HEIGHT, Definitions.BOARD_WIDTH)

    # Initialize scoring and timer
    start_time = time.time()
    ai_score = 0

    # Spawn initial shape
    ai_table.spawn_next_shape()
    placements_left = max_placements - 1

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
            placements_left -= 1

        # Check game over for AI
        if ai_table.game_over or placements_left == 0:
            running = False
            ai_end_time = int(current_time - start_time)
            print(f"AI Score: {ai_score}, Time: {ai_end_time}")

    return ai_score