import curses
import random

#Ask for the players name
player_name = input("Please enter your name:")

#Check if the player has played before:
while True:
    played_before = input("Have you played Snake before? (yes/no)").lower()
    if played_before in {'yes', 'y', 'no', 'n'}:
        break
    else:
        print("Invalid input. Please enter 'yes' or 'no'")

#Instructions for the player if they awnsered no
if played_before in ['no', 'n']:
    print("Welcome to Snake, " + player_name + "! Use the arrow keys to control the snake. You can hold down the arrows to make the snake go faster. Do not let the snake touch the sides of the game area or eat itself! The snake will grow longer each time it eats food. The game will end when the snake runs into the sides of the game area or eats itself. Good luck!")
    input("If you are ready press enter to start the game")

#Deffine Main function
def main(stdscr):
    #Make cursor invisible
    curses.curs_set(0) 
    stdscr.nodelay(1) #Make stscr.getch non blocking
    stdscr.timeout(100) #Refresh screen every 100 ms

    #Get the screen dimensions
    sh, sw = stdscr.getmaxyx() #Screen height and width
    w = curses.newwin(sh, sw, 0, 0) #Create a new window

    # Create the snake position
    snake_x = sw//4
    snake_y = sh//2
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x-1],
        [snake_y, snake_x-2]
    ]
    #Initial food position
    food = [sh//2, sw//2]
    w.addch(int(food[0]), int(food[1]), curses.ACS_PI) # Place the food on the screen

    key = curses.KEY_RIGHT #initial direction of the snake (right)
    score = 0 #Initial score = 0

    while True:
        next_key = w.getch()
        key = key if next_key == -1 else next_key

        if snake[0][0] in [0, sh] or snake[0][1] in [0, sw] or snake[0] in snake[1:]:
            msg = "Game Over! Your score was: " + str(score)
            w.addstr(sh//2, sw//2 - len(msg)//2, msg)
            w.timeout(-1)
            w.getch()
            break #Break the loop to end the game
        
        new_head = [snake[0][0], snake[0][1]]

        #Update snake direction based on key presses
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1
        
        snake.insert(0, new_head)

        #Check if the snake has eaten the food
        if snake[0] == food:
            score += 1
            food = None
            while food is None:
                nf = [
                    random.randint(1, sh-1),
                    random.randint(1, sw-1)
                ]
                food = nf if nf not in snake else None
            w.addch(food[0], food[1], curses.ACS_PI)