import arcade
import random

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCALING_SPRITE = 0.3
DAMAGE_SOUND = arcade.load_sound(':resources:sounds/hurt2.wav')
COIN_COLLECT_SOUND = arcade.load_sound(':resources:sounds/coin5.wav')
LOOSE_SOUND = arcade.load_sound(':resources:sounds/lose5.wav')
WIN_SOUND = arcade.load_sound(':resources:sounds/upgrade4.wav')

class MyGame(arcade.Window):
    """ Our Custom Window Class"""

    def __init__(self):
        """ Initializer """

        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Lab 7 - User Control")
        self.player_sprite = None
        self.coin_sprite = None
        self.stone_sprite = None

        self.player_list = None
        self.coin_list = None
        self.stone_list = None
        self.set_mouse_visible(False)
        self.game_over = False  # Змінна для відстеження стану гри
        self.win = False

    def setup(self):
        arcade.set_background_color(arcade.color.FAWN)
        self.score = 0
        self.live = 3
        self.game_over = False  # Скидаємо стан гри
        self.win = False
        self.player_sprite = arcade.Sprite(':resources:images/space_shooter/playerShip3_orange.png', SCALING_SPRITE)
        self.player_list = arcade.SpriteList()
        self.stone_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        self.coin_list = arcade.SpriteList()

        for _ in range(50):
            coin_sprite = arcade.Sprite(':resources:images/items/coinGold_ll.png', SCALING_SPRITE)
            coin_sprite.center_x = random.randrange(0, 740)
            coin_sprite.center_y = random.randrange(0, 550)
            self.coin_list.append(coin_sprite)

        for _ in range(50):
            stone_sprite = arcade.Sprite(':resources:images/space_shooter/meteorGrey_big2.png', SCALING_SPRITE - 0.1)
            stone_sprite.center_x = random.randrange(0, 740)
            stone_sprite.center_y = random.randrange(0, 550)
            self.stone_list.append(stone_sprite)

    def on_draw(self):
        arcade.start_render()
        self.coin_list.draw()
        self.player_list.draw()
        self.stone_list.draw()
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
        arcade.draw_text(f'Lives: {self.live}', 100, 20, arcade.color.WHITE, 14)

        if self.game_over:
            arcade.draw_text('Game Over. Press E to Restart', 100, 400, arcade.color.WHITE, 32)
        if self.win:
            arcade.draw_text("Congratulations, you won!, E to Restart", 100, 400, arcade.color.WHITE, 32)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """
        if not self.game_over:
            self.player_sprite.center_x = x
            self.player_sprite.center_y = y

    def update(self, delta_time: float):
        if self.game_over:
            return
        elif self.win:
            return

        for coin in self.coin_list:
            coin.center_y += 1
            if coin.center_y > SCREEN_HEIGHT:
                coin.center_y = 0
                coin.center_x = random.randrange(50, SCREEN_WIDTH + 50)

        for stone in self.stone_list:
            stone.center_x += 1
            stone.center_y += random.randrange(-1, 2,)
            if stone.center_x > SCREEN_WIDTH or stone.center_y > SCREEN_HEIGHT:
                stone.center_x = 0

        hit_list_good = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        hit_list_bad = arcade.check_for_collision_with_list(self.player_sprite, self.stone_list)

        for stone in hit_list_bad:
            arcade.play_sound(DAMAGE_SOUND)
            stone.remove_from_sprite_lists()
            self.live -= 1
            if self.live <= 0:
                arcade.play_sound(LOOSE_SOUND)
                self.game_over = True

        for coin in hit_list_good:
            arcade.play_sound(COIN_COLLECT_SOUND)
            coin.remove_from_sprite_lists()
            self.score += 1

        if not self.coin_list:
            arcade.play_sound(WIN_SOUND)
            self.win = True

        self.coin_list.update()
        self.stone_list.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.E and self.game_over:
            self.setup()
        if symbol == arcade.key.E and self.win:
            self.setup()



def main():
    window = MyGame()
    window.setup()
    arcade.run()


main()
