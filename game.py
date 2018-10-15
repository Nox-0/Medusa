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

TODO general: Make the levels, make the character, make the enemies, give each health, implement keys.
TODO after: Add stage progression and menus
Level 1: Completed
Level 2: Not started
Level 3: Not started
Level 4: Not started
Level 5: Not started


TODO ASAP: Health, keys, animations
"""

# Platformer

# Import the arcade and random library
import arcade
import random

# Constants

# Screen sizing assigned here as constants. Measured in pixels.
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Scaling
# This is the scaling for the player sprite
SPRITE_SCALING_PLAYER = 0.92
SPRITE_SCALING_SNAKE = 0.92
SPRITE_SCALING_WALL = 0.92
SPRITE_SCALING_ARROW = 1
SPRITE_PIXEL_SIZE = 70
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * SPRITE_SCALING_WALL)


# Viewport
# How many pixels to leave between player and the edge of the screen
VIEWPORT_MARGIN = 40
RIGHT_MARGIN = 150

# Physics
# Sets the movement speed
MOVEMENT_SPEED = 5
JUMP_SPEED = 14
GRAVITY = 0.7
ARROW_SPEED = 10


class Snake(arcade.Sprite):
	def __init__(self, filename, sprite_scaling):
		super().__init__(filename, sprite_scaling)

		self.change_x = 0

		self.moved = 0
		self.direction = None

		self.health = 0

		self.max_distance = 0
		self.distance = 0

	def update(self):

		# Snake moving mechanics
		if 0 <= self.moved <= 200 and self.direction == "right":
			self.center_x += self.change_x
			self.moved += self.change_x
			self.texture = arcade.load_texture("images/snakeRight.png")

		# Once snake moves X pixels, change the direction
		if self.moved == 200:
			self.direction = "left"

		if self.moved <= 200 and self.direction == "left":
			self.center_x -= self.change_x
			self.moved -= self.change_x
			self.texture = arcade.load_texture("images/snakeLeft.png")

		if self.moved == 0:
			self.direction = "right"


def get_map(filename):
	# Loads an array based on a a .CSV file which is then turned into a map

	# Opens the file
	map_file = open(filename)

	# Creates an empty list that will hold the map
	map_array = []

	# Reads a line from the file
	for line in map_file:
		# Takes away the whitespace and the new lines
		line = line.strip()

		# Creates a list that splits whenever there's a comma (should be after each number)
		map_row = line.split(",")

		# The list is currently all in string format but we want it in integers. ie it is currently "1" and we want it as 1
		# This loop fixes that
		for index, item in enumerate(map_row):
			map_row[index] = int(item)

		# Adds the formatted row into the array
		map_array.append(map_row)

	return map_array


class Game(arcade.Window):
	# This class is the main window of the game

	# Initialiser
	def __init__(self):
		# Calls upon the parent class's initialiser
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Medusa")
		# Initialising the current_stage variable
		self.current_stage = 0

		# Lists for the player, walls, enemies and keys
		self.player_list = None
		self.wall_list = None
		self.snake_list = None
		self.key_list = None
		self.arrow_list = None

		self.snake_count = 0

		self.all_sprites_list = None

		self.player_sprite = None
		self.player_health = 0
		self.player_direction = None

		self.physics_engine = None

		# Used to view port
		self.view_left = 0
		self.view_bottom = 0

		# Right edge of the map (in pixels)
		self.end_of_map = 0

	# Custom method called setup which sets everything up so that the user can play
	def setup(self):

		# Sets the current_stage variable as 0 each setup
		self.current_stage = 1
		# Set the background colour as "AMAZON"
		arcade.set_background_color(arcade.color.AMAZON)

		if self.current_stage == 1:
			self.snake_count = 1
		elif self.current_stage == 2:
			self.snake_count = 5
		elif self.current_stage == 3:
			self.snake_count = 10
		elif self.current_stage == 4:
			self.snake_count = 20

		# Makes the lists into arcade sprite lists which allow us to manipulate them much more easily
		self.player_list = arcade.SpriteList()
		self.wall_list = arcade.SpriteList()
		self.snake_list = arcade.SpriteList()
		self.key_list = arcade.SpriteList()
		self.arrow_list = arcade.SpriteList()
		self.all_sprites_list = arcade.SpriteList()

		for snake in range(self.snake_count):
			snake = Snake("images/snakeRight.png", SPRITE_SCALING_SNAKE)
			snake.change_x = random.randrange(1, 3)

			snake.moved = 0

			if self.current_stage == 1:
				snake.center_x = 1800
				snake.center_y = 128.8

			self.snake_list.append(snake)
			self.all_sprites_list.append(snake)

		# Sets up the player
		self.player_sprite = arcade.AnimatedWalkingSprite()

		# Walking animation
		self.player_sprite.stand_right_textures = []
		self.player_sprite.stand_right_textures.append(arcade.load_texture("images/character.png", scale=SPRITE_SCALING_PLAYER))

		self.player_sprite.stand_left_textures = []
		self.player_sprite.stand_left_textures.append(arcade.load_texture("images/character.png", scale=SPRITE_SCALING_PLAYER, mirrored=True))

		self.player_sprite.walk_right_textures = []
		self.player_sprite.walk_right_textures.append(arcade.load_texture("images/characterw0.png", scale=SPRITE_SCALING_PLAYER))
		self.player_sprite.walk_right_textures.append(arcade.load_texture("images/characterw1.png", scale=SPRITE_SCALING_PLAYER))

		self.player_sprite.walk_left_textures = []
		self.player_sprite.walk_left_textures.append(arcade.load_texture("images/characterw0.png", scale=SPRITE_SCALING_PLAYER, mirrored=True))
		self.player_sprite.walk_left_textures.append(arcade.load_texture("images/characterw1.png", scale=SPRITE_SCALING_PLAYER, mirrored=True))

		self.player_sprite.texture_change_distance = 40

		# Starting positions
		self.player_sprite.center_x = 100
		self.player_sprite.center_y = 270
		self.player_list.append(self.player_sprite)
		self.all_sprites_list.append(self.player_sprite)

		self.player_health = 6

		map_array = get_map("level_1_map.csv")

		# Right edge of the map
		self.end_of_map = len(map_array[0]) * GRID_PIXEL_SIZE

		# Makes an array with each item and what the image is called. It is important to note that arrays start at 0
		map_items = ["grassLeft.png",
		             "grassMid.png",
		             "grassRight.png",
		             "grassCenter.png",
		             "grassHillLeft.png",
		             "grassHillLeft2.png",
		             "lock_green.png"]

		# Loops through array and makes sprites
		for row_index, row in enumerate(map_array):
			for column_index, item in enumerate(row):
				"""
				For this map the numbers represent:
				-1 = empty
				0 = left grass
				1 = middle grass
				2 = right grass
				3 = dirt
				4 = left ramp
				5 = left ramp support
				6 = green lock
				"""
				# If the item is empty then it spawns no sprites there
				if item == -1:
					continue
				else:
					# This is half genius
					# Takes the number from the .csv and then assigns the image in the array that is in that position to wall
					wall = arcade.Sprite("images/" + map_items[item], SPRITE_SCALING_WALL)

					# If the item is a ramp it edits the points of collision and they become as shown
					if item == 4:
						wall.points = ((wall.width // 2, -wall.height // 2),
						               (-wall.width // 2, -wall.height // 2),
						               (wall.width // 2, wall.height // 2))

				# Calculates where the sprite goes
				wall.right = column_index * 64
				wall.top = (7 - row_index) * 64

				# Adds the sprite to the list
				self.all_sprites_list.append(wall)
				self.wall_list.append(wall)

		self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, gravity_constant=GRAVITY)

	# Draws things
	def on_draw(self):
		# Begins to render the game at 60 frames per second
		# This means that it updates the frames 60 times per second, thus creating the illusion of moving objects
		arcade.start_render()

		# Draws all sprites
		self.all_sprites_list.draw()

	def on_key_press(self, key, modifiers):
		# Called whenever a key is pressed
		# Checks for which key is pressed
		if key == arcade.key.UP:
			# Checks if there is a platform beneath the character's feet.
			# You can't jump if you don't have a platform to jump from.
			if self.physics_engine.can_jump():
				self.player_sprite.change_y = JUMP_SPEED
		if key == arcade.key.LEFT:
			self.player_sprite.change_x = -MOVEMENT_SPEED
			self.player_direction = "left"
		if key == arcade.key.RIGHT:
			self.player_sprite.change_x = MOVEMENT_SPEED
			self.player_direction = "right"

		if key == arcade.key.SPACE:
			arrow = arcade.Sprite("images/arrow.png", SPRITE_SCALING_ARROW)

			arrow.center_x = self.player_sprite.center_x
			arrow.center_y = self.player_sprite.center_y
			if self.player_direction == "left":
				arrow.change_x = -ARROW_SPEED
			elif self.player_direction == "right":
				arrow.change_x = ARROW_SPEED

			self.arrow_list.append(arrow)
			self.all_sprites_list.append(arrow)

	def on_key_release(self, key, modifiers):
		# Whenever the a key is released
		# When the left key is released
		if key == arcade.key.LEFT:
			# If the player is already going right, nothing happens
			if self.player_sprite.change_x == MOVEMENT_SPEED:
				pass
			# If the player isn't going right then they stop
			else:
				self.player_sprite.change_x = 0

		if key == arcade.key.RIGHT:
			if self.player_sprite.change_x == -MOVEMENT_SPEED:
				pass
			else:
				self.player_sprite.change_x = 0

	def update(self, delta_time):
		# Same as on_draw method. Renders at 60fps
		# Separate function because here I will cover the movement and game logic

		self.snake_list.update()
		self.arrow_list.update()
		self.all_sprites_list.update_animation()

		if self.player_health == 0:
			self.player_sprite.kill()
			
		for arrow in self.arrow_list:

			snake_hit_list = arcade.check_for_collision_with_list(arrow, self.snake_list)
			wall_hit_list = arcade.check_for_collision_with_list(arrow, self.wall_list)

			hit_list = snake_hit_list + wall_hit_list

			if len(hit_list) > 0:
				arrow.kill()

			for snake in snake_hit_list:
				snake.kill()

		# Updates all of the sprites
		self.physics_engine.update()

		# View port stuff here

		# Checks if view port needs to be changed or not
		changed = False

		# Scroll left
		left_bndry = self.view_left + VIEWPORT_MARGIN
		if self.player_sprite.left < left_bndry:
			self.view_left -= left_bndry - self.player_sprite.left
			changed = True

		# Scroll right
		right_bndry = self.view_left + SCREEN_WIDTH - RIGHT_MARGIN
		if self.player_sprite.right > right_bndry:
			self.view_left += self.player_sprite.right - right_bndry
			changed = True

		# Scroll up
		top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
		if self.player_sprite.top > top_bndry:
			self.view_bottom += self.player_sprite.top - top_bndry
			changed = True

		# Scroll down
		bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
		if self.player_sprite.bottom < bottom_bndry:
			self.view_bottom -= bottom_bndry - self.player_sprite.bottom
			changed = True

		# If we need to scroll, go ahead and do it.
		if changed:
			arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)


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
