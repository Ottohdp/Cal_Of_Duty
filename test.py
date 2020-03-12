# Basic arcade program using objects
# Displays a white window with a blue circle in the middle

# Imports
import arcade
import random

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Cal is on duty"
RADIUS = 50
WIDTH = SCREEN_WIDTH - 20
HEIGHT = SCREEN_HEIGHT - 20
SCALING = 0.7


# Classes
class FlyingSprite(arcade.Sprite):

    def update(self):

        # Move the sprite
        super().update()

        # Remove us if we're off screen
        if self.right < 0:
            self.remove_from_sprite_lists()


class COD(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Setup the empty sprite lists
        self.enemies_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

    def setup(self):
        # Set the background color
        arcade.set_background_color(arcade.color.WHITE)

        # Set up the player
        self.player = arcade.Sprite("images/Cal_front.png", SCALING, image_width=70, image_height=150)
        self.player.center_y = self.height / 2
        self.player.center_x = self.width / 2
        self.all_sprites.append(self.player)

        # Spawn a new enemy every second
        arcade.schedule(self.add_enemy, 1.0)

        self.paused = False
        self.collided = False
        self.collision_timer = 0.0

    def add_enemy(self, delta_time: float):
        # First, create the new enemy sprite
        enemy = arcade.Sprite("images/zombie.png", SCALING, image_width=90, image_height=150)

        # Set its position to a random height and off screen right
        # enemy.left = random.randint(self.width, self.width + 80)
        # enemy.top = random.randint(10, self.height - 10)
        enemy.center_y = self.height / 3
        enemy.center_x = self.width / 3

        # Set its speed to a random speed heading left
        # enemy.velocity = (random.randint(-20, -5), 0)

        # Add it to the enemies list
        self.enemies_list.append(enemy)
        self.all_sprites.append(enemy)

    def on_draw(self):
        # Clear the screen and start drawing
        arcade.start_render()
        # arcade.draw_xywh_rectangle_outline(10, 10, WIDTH, HEIGHT, arcade.color.BLACK)
        # arcade.draw_circle_filled(-1, -1, RADIUS, arcade.color.GRAY)
        # arcade.draw_circle_filled(-1, SCREEN_HEIGHT + 1, RADIUS, arcade.color.GRAY)
        # arcade.draw_circle_filled(SCREEN_WIDTH + 1, SCREEN_HEIGHT + 1, RADIUS, arcade.color.GRAY)
        # arcade.draw_circle_filled(SCREEN_WIDTH + 1, -1, RADIUS, arcade.color.GRAY)
        self.all_sprites.draw()


# Main code entry point
if __name__ == "__main__":
    app = COD(int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), SCREEN_TITLE)
    app.setup()
    arcade.run()
