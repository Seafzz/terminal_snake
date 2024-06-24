import curses
import random

#Ask for the players name
player_name = input("Please enter your name:")

#Check if the player has played before:
while True:
    played_before = input("Have you played Snake before? (yes/no)").lower()
    if played_before in {'yes', 'y' 'no', 'n'}:
        break
    else:
        print("Invalid input. Please enter 'yes' or 'no")

#Instructions for the player if they awnsered no
if played_before in ['no', 'n']:
    print("Welcome to Snake, " + player_name + "! Use the arrow keys to control the snake. You can hold down the arrows to make the snake go faster. Do not let the snake touch the sides of the game area or eat itself! The snake will grow longer each time it eats food. The game will end when the snake runs into the sides of the game area or eats itself. Good luck!")
    input("Press enter to start the game")