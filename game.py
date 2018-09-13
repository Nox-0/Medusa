"""
Level 1:
1 Snake
Green key
Grassy
Is essentially a tutorial

Level 2:
5 Snakes
Orange key
Dirty

Level 3:
10 Snakes
Yellow key
Sandy

Level 4:
20 Snakes
Blue key
Snowy

Level 5:
Medusa
Stony

TODO: Make the levels, make the character, make the enemies, give each health, implement keys
Level 1: In development
Level 2: Not started
Level 3: Not started
Level 4: Not started
Level 5: Not started
"""

# Platformer

# import the arcade library
import arcade

# Screen sizing assigned here as constants. Measured in pixels.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Game(arcade.Window):
	# This class is the main window of the game

	# Initialiser
	def __init__(self):
		# Calls upon the parent class's initialiser
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Medusa")

	# Custom method called setup which sets everything up so that the user can play
	def setup(self):
		# Set the background colour as "AMAZON"
		arcade.set_background_color(arcade.color.AMAZON)

	# Draws things
	def on_draw(self):
		# Begins to render the game at 60 frames per second
		# This means that it updates the frames 60 times per second, thus creating the illusion of moving objects
		arcade.start_render()


# The main function which runs the game
def main():
	window = Game()
	# Runs the setup method before anything else
	window.setup()
	arcade.run()


# If this is the main file, run main()
if __name__ == "__main__":
	main()

"""
This is used due to python being able to import variables and things from other python files and this just
checks to make sure that this is the main file
"""
