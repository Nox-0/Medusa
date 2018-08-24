import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

MAIN_COLOUR_1 = arcade.color.HEART_GOLD
MAIN_COLOUR_2 = arcade.color.GOLDENROD


class Menu(arcade.Window):

	def __init__(self):
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Medusa")
		self.menu_screen = 1

	def start_menu_1(self):
		arcade.set_background_color(MAIN_COLOUR_1)
		arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 600, 300, MAIN_COLOUR_2)
		arcade.draw_text("MEDUSA", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, MAIN_COLOUR_1, 90, align="center", anchor_x="center", anchor_y="center")

	def start_menu_2(self):
		arcade.set_background_color(MAIN_COLOUR_2)
		arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 600, 300, MAIN_COLOUR_1)
		arcade.draw_text("MEDUSA", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, MAIN_COLOUR_2, 90, align="center", anchor_x="center", anchor_y="center")

	def on_draw(self):
		arcade.start_render()

		if self.menu_screen == 1:
			self.start_menu_1()
		elif self.menu_screen == 2:
			self.start_menu_2()

	def on_mouse_press(self, x, y, button, modifiers):
		if button == arcade.MOUSE_BUTTON_LEFT and self.menu_screen == 1 and 100 <= x <= 700 and 150 <= y <= 450:
				self.menu_screen = 2

		elif button == arcade.MOUSE_BUTTON_LEFT and self.menu_screen == 2 and 100 <= x <= 700 and 150 <= y <= 450:
				self.menu_screen = 1


def main():
	window = Menu()
	arcade.run()

main()