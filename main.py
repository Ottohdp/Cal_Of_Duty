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

        self.enemies.list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

    def setup(self):
        self.player = arcade.Sprite("images/Cal_front.png", SCALING)
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

def main():
    game = Cal_On_Duty(WIDTH, HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()
# Display everything

if __name__ == "__main__":
    main()