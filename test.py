# Basic arcade program using objects
# Displays a white window with a blue circle in the middle

# Imports
import arcade

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Cal is on duty"
RADIUS = 50
WIDTH = SCREEN_WIDTH - 20
HEIGHT = SCREEN_HEIGHT - 20
SCALING = 0.7

# Classes
class Welcome(arcade.Window):
    """Main welcome window
    """
    def __init__(self):
        # Call the parent class constructor
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.all_sprites = arcade.SpriteList()

    def on_draw(self):
        """Called whenever you need to draw your window
        """

        # Clear the screen and start drawing
        arcade.start_render()
        arcade.set_background_color(arcade.color.WHITE)
        arcade.draw_xywh_rectangle_outline(10, 10, WIDTH, HEIGHT, arcade.color.BLACK)
        arcade.draw_circle_filled(-1, -1, RADIUS, arcade.color.GRAY)
        arcade.draw_circle_filled(-1, SCREEN_HEIGHT + 1, RADIUS, arcade.color.GRAY)
        arcade.draw_circle_filled(SCREEN_WIDTH + 1, SCREEN_HEIGHT + 1, RADIUS, arcade.color.GRAY)
        arcade.draw_circle_filled(SCREEN_WIDTH + 1, -1, RADIUS, arcade.color.GRAY)
        self.all_sprites.draw()

    def setup(self):
        # Set the background color



        # Set up the player
        self.player = arcade.Sprite("images/Cal_front.png", SCALING, image_width=70, image_height=150)
        self.player.center_y = self.height / 2
        self.player.center_x = self.width / 2
        self.all_sprites.append(self.player)

class COD(arcade.Window):
    "COD... ish"

    def __init__(self, width, height, title):
        """Initialize the game
        """
        super().__init__(width, height, title)

        # Set up the empty sprite lists
        self.enemies_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()




# Main code entry point
if __name__ == "__main__":
    app = Welcome()
    app.setup()
    arcade.run()