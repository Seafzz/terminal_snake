import random
import curses

def player_name(stdscr):
    """
    Function to get the player's name.
    """
    stdscr.clear()
    curses.echo()  # Enable text input
    stdscr.addstr(0, 0, "What's your name? ")
    stdscr.refresh()
    player = stdscr.getstr().decode(encoding="utf-8")
    curses.noecho()  # Disable text input
    return player

def ask_played_before(stdscr):
    """
    Function to ask if the player has played before.
    """
    stdscr.clear()
    stdscr.addstr(0, 0, "Have you played Snake before? (yes/no) ")
    stdscr.refresh()
    while True:
        played_before = stdscr.getstr().decode(encoding="utf-8").lower()
        if played_before in {'yes', 'y', 'no', 'n'}:
            return played_before
        else:
            stdscr.addstr(1, 0, "Invalid input. Please enter 'yes' or 'no'")
            stdscr.refresh()

def print_instructions(stdscr, player):
    """
    Function to print game instructions.
    """
    stdscr.clear()
    stdscr.addstr(0, 0, f"Welcome to Snake, {player}!")
    stdscr.addstr(2, 0, "Use the arrow keys to control the snake. You can hold down the arrows to make the snake go faster.")
    stdscr.addstr(3, 0, "Do not let the snake touch the sides of the game area or eat itself!")
    stdscr.addstr(4, 0, "The snake will grow longer each time it eats food.")
    stdscr.addstr(5, 0, "The game will end when the snake runs into the sides of the game area or eats itself.")
    stdscr.addstr(7, 0, "If you are ready, press enter to start the game.")
    stdscr.refresh()
    stdscr.getch()  # Wait for user input

def main(stdscr):
    # Initialize curses mode
    curses.curs_set(0)  # Make cursor invisible

    # Get the height and width of the screen
    sh, sw = stdscr.getmaxyx()

    # Get player information
    player = player_name(stdscr)
    if ask_played_before(stdscr) in ['no', 'n']:
        print_instructions(stdscr, player)

    # Clear the screen before starting the game loop
    stdscr.clear()

    # Create a new window for the game
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)  # Enable keypad input
    w.timeout(100)  # Refresh every 100 milliseconds

    # Create the snake
    snk_x = sw // 4
    snk_y = sh // 2
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2]
    ]

    # Create the food
    food = [sh // 2, sw // 2]
    w.addch(int(food[0]), int(food[1]), curses.ACS_PI)

    # Initialize the game state
    key = curses.KEY_RIGHT

    # Initialize the score
    score = 0

    while True:
        # Clear the game window
        w.clear()

        # Display the snake and food in the game window
        w.addch(int(food[0]), int(food[1]), curses.ACS_PI)
        for segment in snake:
            w.addch(int(segment[0]), int(segment[1]), curses.ACS_CKBOARD)

        # Get user input for controlling the snake
        next_key = w.getch()
        if next_key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            if (next_key == curses.KEY_UP and key != curses.KEY_DOWN) or \
               (next_key == curses.KEY_DOWN and key != curses.KEY_UP) or \
               (next_key == curses.KEY_LEFT and key != curses.KEY_RIGHT) or \
               (next_key == curses.KEY_RIGHT and key != curses.KEY_LEFT):
                key = next_key

        # Calculate the new head of the snake
        new_head = [snake[0][0], snake[0][1]]

        # Move the snake
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1

        # Insert the new head of the snake
        snake.insert(0, new_head)

        # Check if the snake has eaten the food
        if snake[0] == food:
            score += 1  # Increase the score
            food = None
            while food is None:
                nf = [
                    random.randint(1, sh - 1),
                    random.randint(1, sw - 1)
                ]
                # If the new food position is not part of the snake, place the food there
                food = nf if nf not in snake else None
            w.addch(food[0], food[1], curses.ACS_PI)
        else:
            # Remove the tail of the snake
            tail = snake.pop()
            w.addch(int(tail[0]), int(tail[1]), ' ')

        # Check if game over
        if snake[0][0] in [0, sh] or \
            snake[0][1] in [0, sw] or \
            snake[0] in snake[1:]:
            # End the window
            curses.endwin()
            print(f"Congratulations {player}! Your score is {score}.")
            break

# Initialize curses and start the main game loop
curses.wrapper(main)