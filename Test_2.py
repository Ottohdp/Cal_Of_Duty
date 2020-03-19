# Basic arcade program using objects
# Displays a white window with a blue circle in the middle

# Imports
from typing import Tuple

import arcade
import random

# Constants
SCREEN_WIDTH = 2400
SCREEN_HEIGHT = 1300
SCREEN_TITLE = "Cal is on duty"
WIDTH = SCREEN_WIDTH - 20
HEIGHT = SCREEN_HEIGHT - 20
SCALING = 0.7


# Classes
class FlyingSprite(arcade.Sprite):

    def update(self):

        # Move the sprite
        super().update()

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
        arcade.schedule(self.add_enemy, 0.1)

        self.paused = False
        self.collided = False
        self.collision_timer = 0.0

    def add_enemy(self, delta_time: float):
        # First, create the new enemy sprite
        enemy = arcade.Sprite("images/zombie.png", SCALING, image_width=90, image_height=150)

        for x in range(1):
            spawn = random.randint(1, 4)

            if spawn == 1:
                # Set its position to a random height and off screen right
                enemy.left = random.randint(self.width + 90, self.width + 90)
                enemy.top = random.randint(100, self.height)

                # Set its speed to a random speed heading left
                enemy.velocity = (random.randint(-50, -50), 0)

                # Add it to the enemies list
                self.enemies_list.append(enemy)
                self.all_sprites.append(enemy)

            if spawn == 2:
                # Set its position to a random height and off screen right
                enemy.left = random.randint(0, self.width - 90)
                enemy.top = random.randint(self.height + 150, self.height + 150)

                # Set its speed to a random speed heading left
                enemy.velocity = (random.randint(0, 0), -50)

                # Add it to the enemies list
                self.enemies_list.append(enemy)
                self.all_sprites.append(enemy)

            if spawn == 3:
                # Set its position to a random height and off screen right
                enemy.left = random.randint(-90, -90)
                enemy.top = random.randint(100, self.height)

                # Set its speed to a random speed heading left
                enemy.velocity = (random.randint(50, 50), 0)

                # Add it to the enemies list
                self.enemies_list.append(enemy)
                self.all_sprites.append(enemy)

            if spawn == 4:
                # Set its position to a random height and off screen right
                enemy.left = random.randint(0, self.width - 90)
                enemy.top = random.randint(-150, -150)

                # Set its speed to a random speed heading left
                enemy.velocity = (random.randint(0, 0), 50)

                # Add it to the enemies list
                self.enemies_list.append(enemy)
                self.all_sprites.append(enemy)

    def on_key_press(self, symbol, modifiers):

        if symbol == arcade.key.Q:
            # Quit immediately
            arcade.close_window()

        if symbol == arcade.key.P:
            self.paused = not self.paused

        if symbol == arcade.key.I or symbol == arcade.key.UP:
            self.player.change_y = 90
            arcade.play_sound(self.move_up_sound)

        if symbol == arcade.key.K or symbol == arcade.key.DOWN:
            self.player.change_y = -90
            arcade.play_sound(self.move_down_sound)

        if symbol == arcade.key.J or symbol == arcade.key.LEFT:
            self.player.change_x = -90

        if symbol == arcade.key.L or symbol == arcade.key.RIGHT:
            self.player.change_x = 90

    def on_key_release(self, symbol: int, modifiers: int):

        if (
            symbol == arcade.key.I
            or symbol == arcade.key.K
            or symbol == arcade.key.UP
            or symbol == arcade.key.DOWN
        ):
            self.player.change_y = 0

        if (
            symbol == arcade.key.J
            or symbol == arcade.key.L
            or symbol == arcade.key.LEFT
            or symbol == arcade.key.RIGHT
        ):
            self.player.change_x = 0

    def on_update(self, delta_time: float):
        """Update the positions and statuses of all game objects
        If we're paused, do nothing
        Once everything has moved, check for collisions between
        the player and the list of enemies

        Arguments:
            delta_time {float} -- Time since the last update
        """

        # Did we collide with something earlier? If so, update our timer
        if self.collided:
            self.collision_timer += delta_time
            # If we've paused for two seconds, we can quit
            if self.collision_timer > 2.0:
                arcade.close_window()
            # Stop updating things as well
            return

        # If we're paused, don't update anything
        if self.paused:
            return

        # Did we hit anything? If so, end the game
        #if self.player.collides_with_list(self.enemies_list):
            #self.collided = True
            #self.collision_timer = 0.0

        # Update everything
        for sprite in self.all_sprites:
            sprite.center_x = int(
                sprite.center_x + sprite.change_x * delta_time
            )
            sprite.center_y = int(
                sprite.center_y + sprite.change_y * delta_time
            )
        # self.all_sprites.update()

        # Keep the player on screen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

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
