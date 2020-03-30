import arcade
import random
import pyglet
import pyglet_ffmpeg2

#konstanter
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Hungry cat game"
SCALING = 1.0
spd = input("Hvor svært skal spillet være? (skriv et tal fra 1-5)")
spd = -int(spd)*50
MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 7
player_file = "images/pixil-frame-0.png"
RIGHT_FACING = 0
LEFT_FACING = 1
TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1
SPRITE_SCALING = 0.5


#classes
class Npcsprite(arcade.Sprite):
    """class med alle automatisk bevægende sprites    """

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
        texture = arcade.load_texture("images/pixil-frame-0.png")
        self.textures.append(texture)
        texture = arcade.load_texture("images/pixil-frame-0.png", mirrored=True)
        self.textures.append(texture)
        self.scale = SPRITE_SCALING
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



class cat_game(arcade.Window):
    #spil vinduet
    def __init__(self, width, height, title):

        #skærm dimensioner
        super().__init__(width, height, title)

        #lav tomme sprite lister
        self.points_list = arcade.SpriteList()
        self.danger_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

        self.background = None

        arcade.set_background_color(arcade.color.HOT_MAGENTA)

    def setup(self):
        #gør spillet klar

        # baggrundsfarve
        self.background = arcade.load_texture("images/baggrund.png")

        #kreer karakteren
        self.player = Player()
        self.score = 0
        self.HP = 9
        self.player.center_y = self.height / 2
        self.player.center_x = self.width / 2
        self.all_sprites.append(self.player)

        # Spawn en ny fisk
        arcade.schedule(self.add_point, 1.0)

        # Spawn en ny dråbe
        arcade.schedule(self.add_danger, 1.5)


        # Sørger for at spillet ikke er pauset
        self.paused = False

    def moving(self, direction):
        while True:
            self.player.change_y = direction


    #behandling af tast input
    def on_key_press(self, symbol, modifiers):
        """når en tast trykkes så gør spillet eller spiller spriten den korresponderende handling
        P pauser
        Esc stopper spillet
        WASD styrer spiller spriten
        """

        if symbol == arcade.key.Q:
            arcade.close_window()
            print(self.score)
        if symbol == arcade.key.P:
            self.paused = not self.paused
        if symbol == arcade.key.W:
            self.player.change_y = 250
        if symbol == arcade.key.S:
            self.player.change_y = -250
        if symbol == arcade.key.A:
            self.player.change_x = -250
            #Sprite vendes
            self.player.set_texture(TEXTURE_RIGHT)
        if symbol == arcade.key.D:
            self.player.change_x = 250
            #Sprite vendes:
            self.player.set_texture(TEXTURE_LEFT)

    def on_key_release(self, symbol: int, modifiers: int):
        #hvis der er givet slip på en tast så stopper spriten

        if (symbol == arcade.key.W or symbol == arcade.key.S):
            self.player.change_y = 0

        if (symbol == arcade.key.A or symbol == arcade.key.D):
            self.player.change_x = 0

    def add_point(self, delta_time: float):
        # tilføjer en point givene sprite til skærmen

        # delta_time: {float} kigger på hvor lang tid siden en point sprite blev spawnet sidst

        # spriten laves
        point = Npcsprite("images\pixil-frame-0 (1).png", SCALING*2)

        # sæt start position
        point.center_x = random.randint(self.width, self.width + 10)
        point.center_y = random.randint(50, self.height - 50)

        # sæt hastigheden af spriten
        point.velocity = (spd, 0)

        # tilføj den til spritelisterne
        self.points_list.append(point)
        self.all_sprites.append(point)

    def add_danger(self, delta_time: float):
        # tilføjer en point givene sprite til skærmen
        # spriten laves
        danger = Npcsprite("images/pixil-frame-0 (2).png", SCALING*2)

        # sæt start position
        danger.center_x = random.randint(self.width, self.width + 10)
        danger.center_y = random.randint(50, self.height - 50)

        #hvis en af dråberne rør ved en fisk så ryk dråben
        if danger.collides_with_list(self.points_list):
            danger.remove_from_sprite_lists()

        # sæt hastigheden af spriten
        danger.velocity = (spd, 0)

        # tilføj den til spritelisterne
        self.danger_list.append(danger)
        self.all_sprites.append(danger)



    def on_update(self, delta_time: float):
        #updater og se hvad der er sket

        # Hvis spillet er pauset lad være at gøre noget.
        if self.paused:
            return

        # Har vi ramt en point giver?
        # Så generer en liste over alle point givere vi har ramt.
        phit_list = arcade.check_for_collision_with_list(self.player, self.points_list)

        #gå igennem listen og fjer de ramte sprites
        for point in phit_list:
            point.remove_from_sprite_lists()
            self.score += 1

        # Har vi ramt en fare?
        # Så generer en liste over alle fare sprites vi har ramt.
        dhit_list = arcade.check_for_collision_with_list(self.player, self.danger_list)

        #gå igennem listen og fjer de ramte sprites
        for danger in dhit_list:
            danger.remove_from_sprite_lists()
            self.HP -= 1


        # Opdater alle sprites og ryk dem efter hvor lang tid der er gået
        for sprite in self.all_sprites:
            sprite.center_x = int(
                sprite.center_x + sprite.change_x * delta_time
            )
            sprite.center_y = int(
                sprite.center_y + sprite.change_y * delta_time
            )

        for point in self.points_list:
            if point.right < 0:
                self.HP -= 1
                point.remove_from_sprite_lists()
        #holder spilleren inden for skærmen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0
        if self.HP == 0:
            arcade.close_window()
            print(self.score)
        self.all_sprites.update_animation()


    def on_draw(self):
        """tegn skærmen og alle sprites"""
        arcade.start_render()
        SCALE_B = SCREEN_WIDTH / self.background.width
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.all_sprites.draw()
        # skriv tekst på skærmen
        arcade.draw_text("HP: " + str(self.HP), SCREEN_WIDTH * SCALING -50, 20, arcade.color.WHITE, 14)
        arcade.draw_text("Points: " + str(self.score), 10, 20, arcade.color.WHITE, 14)


if __name__ == "__main__":
    # Create a new Space Shooter window
    Hungry_cat = cat_game(
        int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), SCREEN_TITLE)
    # kald setup
    Hungry_cat.setup()
    # kør spillet
    arcade.run()
