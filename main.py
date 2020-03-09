import arcade
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Cal is on duty"
RADIUS = 50
WIDTH = SCREEN_WIDTH - 20
HEIGHT = SCREEN_HEIGHT - 20
SCALING = 2

# Open the window
arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.set_background_color(arcade.color.WHITE)





class Cal_On_Duty(arcade.Window):
    "Dette er vores take på et Call Of Duty 2d zombies agtigt spil"

    def __init__(self, width , height, title):
        super().__init__(width, height, title)

        self.enemies_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

    def setup(self):
        self.player = arcade.Sprite("Images/Cal_front.png", SCALING)
        self.player.center_y = self.height/2
        self.player.center_x = self.width/2
        self.all_sprites.append(self.player)

    def on_draw(self):

        arcade.start_render()
        self.all_sprites.draw()
    # Laver banen
    arcade.draw_xywh_rectangle_outline(10, 10, WIDTH, HEIGHT, arcade.color.BLACK
    )
    arcade.draw_circle_filled(-1, -1, RADIUS, arcade.color.GRAY
    )
    arcade.draw_circle_filled(-1, SCREEN_HEIGHT+1, RADIUS, arcade.color.GRAY
    )
    arcade.draw_circle_filled(SCREEN_WIDTH+1, SCREEN_HEIGHT+1, RADIUS, arcade.color.GRAY
    )
    arcade.draw_circle_filled(SCREEN_WIDTH+1, -1, RADIUS, arcade.color.GRAY
    )
# note her
class Welcome(arcade.Window):
    def __init__(self):
        "Initialize the window"
        # Call the parent class constructor
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

# Main code entry point
if __name__ == "__main__":
    app = Welcome()
    arcade.run()
