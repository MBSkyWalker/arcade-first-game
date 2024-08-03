""" Lab 7 - User Control """

import arcade

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SCALING = 0.5
CHARACTER_MOVEMENT_SPEED = 5
class Character(arcade.Sprite):
    def __init__(self, image_path, scaling):
        super().__init__(image_path, scaling)
        self.speed = CHARACTER_MOVEMENT_SPEED
        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

    def move_left(self):
        self.change_x = -self.speed

    def move_right(self):
        self.change_x = self.speed

    def stop_moving(self):
        self.change_x = 0


class MyGame(arcade.Window):
    """ Our Custom Window Class"""

    def __init__(self):
        """ Initializer """

        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Lab 7 - User Control")
        self.tile_map = None
        self.wall_list = None
        self.character = None
        self.character2 = None



    def setup(self):
        self.wall_list = arcade.SpriteList()
        map_name = 'maps/map2.json'
        self.tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)
        self.wall_list = self.tile_map.sprite_lists['map2']
        self.character = Character('images/tank_dark_right.png', 2)
        self.character2 = Character(':resources:images/animated_characters/zombie/zombie_idle.png', 1)
        self.character2.center_x = 500
        self.character2.center_y = 125
        self.character.center_x = 100
        self.character.center_y = 105
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

    def on_draw(self):
        arcade.start_render()
        self.wall_list.draw()
        self.character.draw()
        self.character2.draw()

    def on_update(self, delta_time: float):
        self.character.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D:
            self.character.move_right()

        elif symbol == arcade.key.A:
            self.character.move_left()


    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D:
            self.character.stop_moving()

        elif symbol == arcade.key.A:
            self.character.stop_moving()
def main():
    window = MyGame()
    window.setup()
    arcade.run()


main()