import arcade
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Lab 7 - User Control")
        self.tile_map = None



    def setup(self):

        map_name = 'maps/shooter_map.json'
        self.tile_map = arcade.load_tilemap(map_name)
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        else:
            arcade.set_background_color(arcade.color.AMAZON)




    def on_draw(self):
        arcade.start_render()




def main():
    window = MyGame()
    window.setup()
    arcade.run()


main()