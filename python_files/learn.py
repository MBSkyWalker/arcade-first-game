import arcade
import random

DEFAULT_SCREEN_WIDTH = 1280
DEFAULT_SCREEN_HEIGHT = 720
SCALING_TANK = 0.9
SCALING_WALL = 0.6
MOVEMENT_SPEED = 5
ANGLE_SPEED = 5
VIEWPORT_MARGIN = 220
CAMERA_SPEED = 0.1
TILE_SCALING = 0.5
map_name = 'lvl.json'
GRAVITY = 0.25
PLAYER_MOVEMENT_SPEED = 7
JUMP_SPEED = 10

class Mygame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        # sprite lists
        self.player_list = None
        self.wall_list = None
        self.left_pressed = False
        self.right_pressed = False
        self.player_sprite = None
        self.walls_sprite = None
        self.bullet_sprite = None
        self.bullet_list = None

        self.physics_engine = None

        self.tile_map = None

        # Create the cameras. One for the GUI, one for the sprites.
        self.camera_sprites = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)


    def setup(self):
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)
        # set up the player sprites list
        self.player_list = arcade.SpriteList()
        # set up the wall sprites list
        self.wall_list = arcade.SpriteList()
        # set the score
        self.score = 0
        # Create the player
        self.player_sprite = arcade.Sprite(':resources:images/animated_characters/female_person/femalePerson_walk4.png', SCALING_TANK)
        self.player_sprite.center_x = 200
        self.player_sprite.center_y = 119
        self.player_list.append(self.player_sprite)

        #set the map name
        map_name = 'maps/lvl.json'
        self.tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)

        # Set wall and coin SpriteLists
        # Any other layers here. Array index must be a layer.
        self.wall_list = self.tile_map.sprite_lists["walls"]

        # --- Other stuff
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Keep player from running through the wall_list layer
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            self.wall_list,
            gravity_constant=GRAVITY
        )

    def on_draw(self):
        self.clear()
        arcade.start_render()
        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()

        # Draw all the sprites.
        self.wall_list.draw()
        self.player_list.draw()

        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()

    def update(self, delta_time: float):
        # self.physics_engine.update()
        CAMERA_SPEED = 1
        lower_left_corner = (self.player_sprite.center_x - self.width / 2,
                             self.player_sprite.center_y - self.height / 2)
        self.camera_sprites.move_to(lower_left_corner, CAMERA_SPEED)


    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False


    def on_update(self, delta_time):
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        # self.player_sprite.change_y = 0

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        # Scroll the screen to the player
        self.scroll_to_player()


    def scroll_to_player(self):
        """
        Scroll the window to the player.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a
        smoother pan.
        """

        position = self.player_sprite.center_x - self.width / 2, \
                   self.player_sprite.center_y - self.height / 2
        self.camera_sprites.move_to(position, CAMERA_SPEED)


    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))


def main():
    """ Main function """
    window = Mygame(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, "My game")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()