import random
from pyglet.math import Vec2
import arcade

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCALING_SPRITE = 0.3
TILE_SIZE = 128 * SCALING_SPRITE  # Розмір плитки
MOVEMENT_SPEED = 2
VIEW_PORT_MARGIN = 100
CAMERA_SPEED = 0.1
NUMBER_OF_COINS = 20
UPDATES_PER_FRAME = 5
RIGHT_FACING = 0
LEFT_FACING = 1
def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]
class PlayerCharacter(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0

        self.scale = SCALING_SPRITE

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)


        # --- Load Textures ---

        # Images from Kenney.nl's Asset Pack 3
        main_path = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"
        # main_path = ":resources:images/animated_characters/female_person/femalePerson"
        # main_path = ":resources:images/animated_characters/male_person/malePerson"
        # main_path = ":resources:images/animated_characters/male_adventurer/maleAdventurer"
        # main_path = ":resources:images/animated_characters/zombie/zombie"
        # main_path = ":resources:images/animated_characters/robot/robot"
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.walk_textures = [load_texture_pair(f"{main_path}_walk{i}.png") for i in range(8)]

        # Load textures for idle standing
        self.texture = self.idle_texture_pair[RIGHT_FACING]

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.walk_textures[frame][direction]
class MyGame(arcade.Window):
    """ Our Custom Window Class"""

    def __init__(self):
        """ Initializer """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Wall Creation")
        self.wall_list = None
        self.player_list = None
        self.player_sprite = None
        self.physics_engine = None
        self.coin_sprite = None
        self.coin_list = None
        self.scale = 1.0
        # Camera initialization
        self.player_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.gui_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)


    def setup(self):
        arcade.set_background_color(arcade.color.COOL_GREY)
        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = SCREEN_HEIGHT / 2 - 30
        self.player_list.append(self.player_sprite)
        self.score = 0


        self.coin_list = arcade.SpriteList()
        # Створення нижньої стіни
        for x in range(0, SCREEN_WIDTH, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/dirtCenter_rounded.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = TILE_SIZE / 2
            self.wall_list.append(wall)

        # Створення верхньої стіни
        for x in range(0, SCREEN_WIDTH, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/dirtCenter_rounded.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = SCREEN_HEIGHT - TILE_SIZE / 2
            self.wall_list.append(wall)

        # Створення лівої стіни
        for y in range(0, SCREEN_HEIGHT, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/dirtCenter_rounded.png", SCALING_SPRITE)
            wall.center_x = TILE_SIZE / 2
            wall.center_y = y + TILE_SIZE / 2
            self.wall_list.append(wall)
        center_start = SCREEN_HEIGHT // 2 - TILE_SIZE * 2
        center_end = SCREEN_HEIGHT // 2 + TILE_SIZE * 2
        # Створення правої стіни

        for y in range(0, SCREEN_HEIGHT, int(TILE_SIZE)):
            if center_start <= y <= center_end:
                continue
            wall = arcade.Sprite(":resources:images/tiles/dirtCenter_rounded.png", SCALING_SPRITE)
            wall.center_x = SCREEN_WIDTH - TILE_SIZE / 2
            wall.center_y = y + TILE_SIZE / 2

            self.wall_list.append(wall)
        # First row
        for x in range(50 + int(TILE_SIZE), 200, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = 300
            self.wall_list.append(wall)

        for x in range(200 + int(TILE_SIZE), 500, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = 300
            self.wall_list.append(wall)


        for x in range(500 + int(TILE_SIZE), 730, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = 300
            self.wall_list.append(wall)
        # Second row
        for x in range(100 + int(TILE_SIZE), 200, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = 200
            self.wall_list.append(wall)

        for x in range(270 + int(TILE_SIZE), 309, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = 200
            self.wall_list.append(wall)

        for x in range(350 + int(TILE_SIZE), 500, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = 200
            self.wall_list.append(wall)

        for x in range(500 + int(TILE_SIZE), 580, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = 200
            self.wall_list.append(wall)
        # Thirst row
        for x in range(100 + int(TILE_SIZE), 250, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = 100
            self.wall_list.append(wall)

        for x in range(270 + int(TILE_SIZE), 309, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = 100
            self.wall_list.append(wall)

        for x in range(350 + int(TILE_SIZE), 500, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = 100
            self.wall_list.append(wall)

        for x in range(500 + int(TILE_SIZE), 700, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = 100
            self.wall_list.append(wall)

        # fourth row
        for x in range(100 + int(TILE_SIZE), 200, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = 500
            self.wall_list.append(wall)

        for x in range(270 + int(TILE_SIZE), 340, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = 500
            self.wall_list.append(wall)

        for x in range(350 + int(TILE_SIZE), 500, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = 500
            self.wall_list.append(wall)

        for x in range(500 + int(TILE_SIZE), 580, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = 500
            self.wall_list.append(wall)

        #last row
        for x in range(100 + int(TILE_SIZE), 200, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = 400
            self.wall_list.append(wall)

        for x in range(270 + int(TILE_SIZE), 309, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = 400
            self.wall_list.append(wall)

        for x in range(350 + int(TILE_SIZE), 500, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = 400
            self.wall_list.append(wall)

        for x in range(500 + int(TILE_SIZE), 580, int(TILE_SIZE)):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SCALING_SPRITE)
            wall.center_x = x + TILE_SIZE / 2
            wall.center_y = 400
            self.wall_list.append(wall)
        # Collision with walls
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         self.wall_list)
        for i in range(NUMBER_OF_COINS):
            coin = arcade.Sprite(':resources:images/items/gemBlue.png', SCALING_SPRITE)
        # --- IMPORTANT PART ---

        # Boolean variable if we successfully placed the coin
            coin_placed_successfully = False

            # Keep trying until success
            while not coin_placed_successfully:
                # Position the coin
                coin.center_x = random.randrange(SCREEN_WIDTH)
                coin.center_y = random.randrange(SCREEN_HEIGHT)

                # See if the coin is hitting a wall
                wall_hit_list = arcade.check_for_collision_with_list(coin, self.wall_list)

                # See if the coin is hitting another coin
                coin_hit_list = arcade.check_for_collision_with_list(coin, self.coin_list)

                if len(wall_hit_list) == 0 and len(coin_hit_list) == 0:
                    # It is!
                    coin_placed_successfully = True

            # Add the coin to the lists
            self.coin_list.append(coin)

        # --- END OF IMPORTANT PART ---
    def on_draw(self):
        arcade.start_render()
        self.player_camera.use()
        self.wall_list.draw()
        self.player_list.draw()
        self.coin_list.draw()
        self.gui_camera.use()
        output = f"Score: {self.score}"
        arcade.draw_text(output, 80, 70, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
    def on_update(self, delta_time: float):
        self.physics_engine.update()
        self.scroll_to_player()
        self.player_list.update_animation()
        hit_list_good = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in hit_list_good:
            # arcade.play_sound(COIN_COLLECT_SOUND)
            coin.remove_from_sprite_lists()
            self.score += 1

    def scroll_to_player(self):
        """
        Scroll the window to the player.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a smoother
        pan.
        """

        position = Vec2(self.player_sprite.center_x - self.width / 2,
                        self.player_sprite.center_y - self.height / 2)
        self.player_camera.move_to(position, CAMERA_SPEED)

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.player_camera.resize(int(width), int(height))
        self.gui_camera.resize(int(width), int(height))
def main():
    window = MyGame()
    window.setup()
    arcade.run()

main()
