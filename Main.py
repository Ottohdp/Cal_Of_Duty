# Basic arcade program using objects
# Displays a white window with a blue circle in the middle

# Imports
from typing import Tuple

import arcade
import random
import time

# Constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Cal is on duty"
RADIUS = 50
WIDTH = SCREEN_WIDTH - 20
HEIGHT = SCREEN_HEIGHT - 20
SCALING = 0.7
CHARACTER_SCALING = 0.7
BULLET_SPEED = 50

RIGHT_FACING = 0
LEFT_FACING = 1
TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1


# Classes
class Npcsprite(arcade.Sprite):

    def update(self):
        # ryk sprites
        super().update()

        # Fjern en sprite hvis den er uden for skærmen.
        if self.right < 0:
            self.remove_from_sprite_lists()


class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()

        self.textures = []
        # Load a left facing texture and a right facing texture.
        # mirrored=True will mirror the image we load.
        texture = arcade.load_texture("images/Cal_hjre.png")
        self.textures.append(texture)
        texture = arcade.load_texture("images/Cal_hjre.png", mirrored=True)
        self.textures.append(texture)
        self.scale = CHARACTER_SCALING
        # By default, face right.
        self.set_texture(TEXTURE_RIGHT)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        # Figure out if we should face left or right
        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_RIGHT]
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

class COD(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Setup the empty sprite lists
        self.enemies_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

        # Set the background color
        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):

        # Set up the player
        self.player_sprite = Player()
        self.player_sprite.center_y = self.height / 2
        self.player_sprite.center_x = self.width / 2
        self.all_sprites.append(self.player_sprite)

        # Spawn a new enemy every second
        arcade.schedule(self.add_enemy, 0.5)

        self.paused = False
        self.collided = False
        self.collision_timer = 0.0

    def moving(self, direction):
        while True:
            self.player.change_y = direction

    def add_enemy(self, delta_time: float):
        # First, create the new enemy sprite
        enemy = arcade.Sprite("images/zombie.png", SCALING, image_width=90, image_height=150)

        for x in range(1):
            spawn = random.randint(1, 1)

            if spawn == 1:
                # Set its position to a random height and off screen right
                enemy.left = random.randint(self.width + 90, self.width + 90)
                enemy.top = random.randint(100, self.height)

                enemy.velocity = (random.randint(-50, -50), 0)

                # Add it to the enemies list
                self.enemies_list.append(enemy)
                self.all_sprites.append(enemy)

            # if spawn == 2:
            # Set its position to a random height and off screen right
            # enemy.left = random.randint(0, self.width - 90)
            # enemy.top = random.randint(self.height + 150, self.height + 150)

            # Set its speed to a random speed heading left
            # enemy.velocity = (random.randint(0, 0), -50)

            # Add it to the enemies list
            # self.enemies_list.append(enemy)
            # self.all_sprites.append(enemy)

            # if spawn == 3:
            # Set its position to a random height and off screen right
            # enemy.left = random.randint(-90, -90)
            # enemy.top = random.randint(100, self.height)

            # Set its speed to a random speed heading left
            # enemy.velocity = (random.randint(50, 50), 0)

            # Add it to the enemies list
            # self.enemies_list.append(enemy)
            # self.all_sprites.append(enemy)

            # if spawn == 4:
            # Set its position to a random height and off screen right
            # enemy.left = random.randint(0, self.width - 90)
            # enemy.top = random.randint(-150, -150)

            # Set its speed to a random speed heading left
            # enemy.velocity = (random.randint(0, 0), 50)

            # Add it to the enemies list
            # self.enemies_list.append(enemy)
            # self.all_sprites.append(enemy)

    def on_key_press(self, symbol, modifiers):

        if symbol == arcade.key.Q:
            # Quit immediately
            arcade.close_window()

        if symbol == arcade.key.P:
            self.paused = not self.paused

        if symbol == arcade.key.W or symbol == arcade.key.UP:
            self.player_sprite.change_y = 180

        if symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.player_sprite.change_y = -180

        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.player_sprite.change_x = -180
            # Sprite vendes
            self.player_sprite.set_texture(TEXTURE_RIGHT)

        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.player_sprite.change_x = 180
            # Sprite vendes:
            self.player_sprite.set_texture(TEXTURE_LEFT)

        if symbol == arcade.key.SPACE:
            # Create a bullet
            bullet = arcade.Sprite("images/skud.png", SCALING, image_width=30, image_height=10)
            bullet_angle = 0
            bullet.change_x = BULLET_SPEED
            bullet.center_x = self.player_sprite.center_y
            bullet.bottom = self.player_sprite.right
            self.bullet_list.append(bullet)

    def on_key_release(self, symbol: int, modifiers: int):

        if (
                symbol == arcade.key.W
                or symbol == arcade.key.S
                or symbol == arcade.key.UP
                or symbol == arcade.key.DOWN
        ):
            self.player_sprite.change_y = 0

        if (
                symbol == arcade.key.A
                or symbol == arcade.key.D
                or symbol == arcade.key.LEFT
                or symbol == arcade.key.RIGHT
        ):
            self.player_sprite.change_x = 0

    def on_update(self, delta_time: float):
        """Update the positions and statuses of all game objects
        If we're paused, do nothing
        Once everything has moved, check for collisions between
        the player and the list of enemies

        Arguments:
            delta_time {float} -- Time since the last update
        """

        self.bullet_list.update()
        for bullet in self.bullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemies_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            for enemy in hit_list:
                enemy.remove_from_sprite_lists()

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > SCREEN_WIDTH:
                bullet.remove_from_sprite_lists()

        liv = 3
        # Did we collide with something earlier? If so, update our timer
        if self.collided:
            self.collision_timer += delta_time
            # If we've paused for two seconds, we can quit
            if self.collision_timer > 2.0:
                liv = liv - 1
                time.sleep(3)
            if liv == 0:
                arcade.close_window()

            # Stop updating things as well
            return

        # If we're paused, don't update anything
        if self.paused:
            return

        # Did we hit anything? If so, end the game
        if self.player_sprite.collides_with_list(self.enemies_list):
            self.collided = True
            self.collision_timer = 0.0

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
        if self.player_sprite.top > self.height:
            self.player_sprite.top = self.height
        if self.player_sprite.right > self.width:
            self.player_sprite.right = self.width
        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0

    def on_draw(self):
        # Clear the screen and start drawing
        arcade.start_render()
        # arcade.draw_xywh_rectangle_outline(10, 10, WIDTH, HEIGHT, arcade.color.BLACK)
        # arcade.draw_circle_filled(-1, -1, RADIUS, arcade.color.GRAY)
        # arcade.draw_circle_filled(-1, SCREEN_HEIGHT + 1, RADIUS, arcade.color.GRAY)
        # arcade.draw_circle_filled(SCREEN_WIDTH + 1, SCREEN_HEIGHT + 1, RADIUS, arcade.color.GRAY)
        # arcade.draw_circle_filled(SCREEN_WIDTH + 1, -1, RADIUS, arcade.color.GRAY)
        self.all_sprites.draw()
        self.bullet_list.draw()



# Main code entry point
if __name__ == "__main__":
    app = COD(int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), SCREEN_TITLE)
    app.setup()
    arcade.run()
