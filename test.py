import arcade
import random
import logging

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCALING_KNIFE = 0.5
SCALING_WOOD = 0.3
# sound_wood_knife = arcade.load_sound(':resources:sounds/hit3.wav')
scream_sound = arcade.load_sound('sound/scream-with-echo-46585.mp3')
random_spawn = random.randrange(0, 600)

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_WIDTH, 'PR')
        self.game_over = False
        self.knife_list = None
        self.wood_list = None
        self.knife_sprite = None
        self.wood_sprite = None
        self.score = 0
        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)

    def setup(self):
        self.knife_list = arcade.SpriteList()
        self.wood_list = arcade.SpriteList()
        self.score = 0
        self.game_over_image = arcade.load_texture("images/screamer.png")
        self.knife_sprite = arcade.Sprite('images/coin_01.png', SCALING_KNIFE)
        self.knife_sprite.center_x = 400
        self.knife_sprite.center_y = 100
        self.knife_sprite.change_y = 0
        self.knife_sprite.change_x = 10
        self.wood_sprite = arcade.Sprite('images/wood.png', SCALING_WOOD)
        self.wood_sprite.center_x = random_spawn
        self.wood_sprite.center_y = 600
        self.knife_list.append(self.knife_sprite)
        self.wood_list.append(self.wood_sprite)



    # def draw_new_wood(self):
    #     wood = self.wood_sprite
    #     wood.center_x = self.wood_sprite.center_x
    #     wood.center_y = self.wood_sprite.center_y
    #     self.wood_list.append(wood)

    def update(self, delta_time: float):
        self.knife_sprite.center_y += self.knife_sprite.change_y
        self.knife_sprite.center_x += self.knife_sprite.change_x
        if self.knife_sprite.center_x > SCREEN_WIDTH:
            self.knife_sprite.change_x *= -1


        if self.knife_sprite.center_x < 0:
            self.knife_sprite.center_x_ = 0
            self.knife_sprite.change_x *= -1

        if self.knife_sprite.center_y > SCREEN_HEIGHT + 300:
            self.knife_sprite.center_y = 100
            self.knife_sprite.change_y = 0

        self.knife_list.update()
        self.wood_list.update()

        collision_check = arcade.check_for_collision_with_list(self.knife_sprite, self.wood_list)
        if collision_check:
            if self.score < 10:
                # arcade.play_sound(self.sound_wood_knife)
                self.score += 1
                for wood in collision_check:
                    random_spawn_x = random.randint(50, SCREEN_WIDTH - 50)
                    random_spawn_y = random.randint(50, SCREEN_HEIGHT - 50)
                    wood.center_x = random_spawn_x
                    wood.center_y = 600
            else:

                arcade.play_sound(scream_sound)
                self.game_over = True
                for wood in self.wood_list:
                    wood.remove_from_sprite_lists()


                print('game ended')







    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W or symbol == arcade.key.SPACE:
            logging.warning('Key space get pressed')
            self.knife_sprite.change_y = 10

    def on_draw(self):
        arcade.start_render()

        if self.game_over:
            # Відображення фону при завершенні гри
            arcade.draw_texture_rectangle(
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                self.game_over_image
            )
            arcade.draw_text('THE END', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.BLACK, 50, anchor_x='center',
                             anchor_y='center')
        else:
            output = f'Score: {self.score}'
            arcade.draw_text(output, 20, 30, arcade.color.BLACK, 24)
            self.knife_list.draw()
            self.wood_list.draw()




def main():
    window = MyGame()
    window.setup()
    arcade.run()


main()
