# Imports
import arcade
import random
import time
import math

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
zombieSpeed = 50
TEXTURE_RIGHT = 0
TEXTURE_LEFT = 1
TEXTURE_UP = 2
TEXTURE_DOWN = 3

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]

# Classes
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
        texture = arcade.load_texture("images/Cal_bag.png")
        self.textures.append(texture)
        texture = arcade.load_texture("images/Cal_front.png")
        self.textures.append(texture)
        self.scale = CHARACTER_SCALING
        # By default, face right.
        self.set_texture(TEXTURE_RIGHT)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        # Figure out if we should face left or right
        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_RIGHT]
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_LEFT]
        if self.change_y < 0:
            self.texture = self.textures[TEXTURE_UP]
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_DOWN]


class Enemy(arcade.Sprite):
    def __init__(self, player_sprite):
        super().__init__()
        self.player_sprite = player_sprite
        self.scale = 0.7
        texture_list = []
        main_path = "Images/zombie.png"
        texture_list.append(main_path)
        self.idle_texture_pair = load_texture_pair(texture_list[0])
        self.texture = self.idle_texture_pair[1]

    def update_animation(self, delta_time: float = 1/60):
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[1]
            return

    def follow_sprite(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if random.randrange(100) == 0:
            start_x = self.center_x
            start_y = self.center_y

            dest_x = self.player_sprite.center_x
            dest_y = self.player_sprite.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            self.change_x = math.cos(angle) * 1
            self.change_y = math.sin(angle) * 1




class COD(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Setup the empty sprite lists
        self.enemies_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

        # Set the background color
        arcade.set_background_color(arcade.color.WHITE)

        self.score = 0

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
        self.HP = 3
        self.score = 0

    def on_key_press(self, symbol, modifiers):

        if symbol == arcade.key.Q:
            # Quit immediately
            arcade.close_window()

        if symbol == arcade.key.P:
            self.paused = not self.paused

        if symbol == arcade.key.W or symbol == arcade.key.UP:
            self.player_sprite.change_y = 180
            # Sprite vendes
            self.player_sprite.set_texture(TEXTURE_UP)

        if symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.player_sprite.change_y = -180
            # Sprite vendes
            self.player_sprite.set_texture(TEXTURE_DOWN)

        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.player_sprite.change_x = -180
            # Sprite vendes
            self.player_sprite.set_texture(TEXTURE_LEFT)

        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.player_sprite.change_x = 180
            # Sprite vendes:
            self.player_sprite.set_texture(TEXTURE_RIGHT)

        if symbol == arcade.key.SPACE:
            bullet = arcade.Sprite("images/skud.png", SCALING, image_width=10, image_height=10)
            bullet.change_x = 0
            bullet.change_y = 0
            bullet.center_x = self.player_sprite.center_x
            bullet.center_y = self.player_sprite.center_y
            self.bullet_list.append(bullet)

            if self.player_sprite.texture == self.player_sprite.textures[0]:
                bullet.change_x = 50

            if self.player_sprite.texture == self.player_sprite.textures[1]:
                bullet.change_x = -50

            if self.player_sprite.texture == self.player_sprite.textures[2]:
                bullet.change_y = 50

            if self.player_sprite.texture == self.player_sprite.textures[3]:
                bullet.change_y = -50

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

    def add_enemy(self, delta_time: float):
        # First, create the new enemy sprite
        enemy = Enemy(self.player_sprite)

        for x in range(1):
            spawn = random.randint(1, 1)

            if spawn == 1:
                # Set its position to a random height and the right side of the screen
                enemy.left = random.randint(self.width + 90, self.width + 90)
                enemy.top = random.randint(100, self.height)


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

    def on_update(self, delta_time: float):
        self.enemies_list.update()
        self.enemies_list.update_animation()

        for enemy in self.enemies_list:
            enemy.follow_sprite()

        self.bullet_list.update()
        for bullet in self.bullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemies_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.score += 1

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > SCREEN_WIDTH:
                bullet.remove_from_sprite_lists()

        if self.HP == 0:
            time.sleep(2)
            arcade.close_window()
        # Did we collide with something earlier? If so, update our timer
        if self.collided:
            for enemy in self.enemies_list:

                enemy_hit = arcade.check_for_collision_with_list(self.player_sprite, self.enemies_list)

                if len(enemy_hit) > 0:
                    enemy.remove_from_sprite_lists()

                for enemy in enemy_hit:
                    enemy.remove_from_sprite_lists()

                    self.collided = False
                    self.HP -= 1


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
        self.all_sprites.draw()
        self.bullet_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)

        output = f"Lives: {self.HP}"
        arcade.draw_text(output, 10, 40, arcade.color.RED, 20)


# Main code entry point
if __name__ == "__main__":
    app = COD(int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), SCREEN_TITLE)
    app.setup()
    arcade.run()
