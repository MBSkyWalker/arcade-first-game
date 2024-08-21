import random
import time

import arcade
import math
from Enemys.enemys import Enemy, Kamikaze, GrenadeLauncher, Explosion, Prospector
from pyglet.math import Vec2
import timeit
import os
SCREEN_WIDTH = 1680
SCREEN_HEIGHT = 1050
MOVEMENT_SPEED = 3
CAMERA_SPEED = 0.1
GRAVITY = 0.25
SPRITE_SCALING_BULLET = 0.8
BULLET_SPEED = 10
COIN_SOUND = arcade.load_sound(':resources:sounds/coin1.wav')
ENEMY_SOUND = arcade.load_sound(':resources:sounds/fall4.wav')
ENEMY_SHOOT_SOUND = arcade.load_sound(':resources:sounds/laser2.wav')
PISTOL_SHOOT_SOUND = arcade.load_sound(':resources:sounds/laser3.wav')
HURT_PLAYER_SOUND = arcade.load_sound(':resources:sounds/hurt3.wav')
MUSIC = arcade.load_sound('sound/Damjan Mravunac - The Grand Cathedral.mp3')
ENEMY_HURT_SOUND = arcade.load_sound(':resources:sounds/hurt2.wav')
PISTOL_AMMO = 10
RELOAD_SOUND = arcade.load_sound(':resources:sounds/upgrade1.wav')
EXPLOSION_SOUND = arcade.load_sound('sound/medium-explosion-40472.mp3')
file_path = 'shooter_images/PNG/Hitman 1/hitman1_gun.png'
print(os.path.isfile(file_path))


class Win(arcade.View):
    def __init__(self, player_camera):
        super().__init__()
        self.player_camera = player_camera

    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        camera_x, camera_y = self.player_camera.position
        arcade.start_render()
        arcade.draw_text("You won, Congratulations!", camera_x + SCREEN_WIDTH / 2, camera_y + SCREEN_HEIGHT / 2 + 50,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
        arcade.draw_text("press space to restart", camera_x + SCREEN_WIDTH / 2, camera_y + SCREEN_HEIGHT / 2 - 50,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            game_view = MyGame()
            game_view.window.set_mouse_visible(False)
            game_view.setup()
            self.window.show_view(game_view)


class GameOver(arcade.View):
    def __init__(self, player_camera):
        super().__init__()
        self.player_camera = player_camera

    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        camera_x, camera_y = self.player_camera.position
        arcade.start_render()
        arcade.draw_text("You lost", camera_x + SCREEN_WIDTH / 2, camera_y + SCREEN_HEIGHT / 2 + 50,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
        arcade.draw_text("press space to restart", camera_x + SCREEN_WIDTH / 2, camera_y + SCREEN_HEIGHT / 2 - 50,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            game_view = MyGame()
            game_view.window.set_mouse_visible(False)
            game_view.setup()
            self.window.show_view(game_view)


class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Welcome to my first serious game! Press mouse to shoot", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
        arcade.draw_text('Your goal is to collect all gems', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50, arcade.color.WHITE,
                         font_size=20, anchor_x='center')
        arcade.draw_text("Click to Start", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = MyGame()
        game_view.window.set_mouse_visible(False)
        game_view.setup()
        self.window.show_view(game_view)


class Player(arcade.Sprite):
    def __init__(self, image, scale, player_camera):
        super().__init__(image, scale)
        self.change_x = 0
        self.change_y = 0
        self.lives = 10
        self.player_camera = player_camera
        self.ammo = 10
        self.is_reloading = False
        self.reload_time = 1

    def update(self, target_x, target_y):
        self.center_x += self.change_x
        self.center_y += self.change_y

        delta_x = target_x - self.center_x
        delta_y = target_y - self.center_y

        angle = math.degrees(math.atan2(delta_y, delta_x))
        self.angle = angle

    def shoot(self, x, y, bullet_list, pistol_shoot_sound):

        if self.ammo > 0:
            #  Додаємо зміщення камери до координат миші для правильного обчислення кута
            adjusted_x = x + self.player_camera.position[0]
            adjusted_y = y + self.player_camera.position[1]

            # Створюємо кулю
            bullet = arcade.Sprite("shooter_images/PNG/Tiles/tile_187.png", SPRITE_SCALING_BULLET)

            # Позиціонуємо кулю на поточній локації гравця
            start_x = self.center_x
            start_y = self.center_y
            bullet.center_x = start_x
            bullet.center_y = start_y

            # Обчислюємо різницю в координатах для обчислення кута
            x_diff = adjusted_x - start_x
            y_diff = adjusted_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Куля летить під правильним кутом
            bullet.angle = math.degrees(angle)

            # Встановлюємо зміну положення кулі
            bullet.change_x = math.cos(angle) * BULLET_SPEED
            bullet.change_y = math.sin(angle) * BULLET_SPEED
            arcade.play_sound(pistol_shoot_sound)
            # Додаємо кулю до списку
            bullet_list.append(bullet)

            self.ammo -= 1
        else:

            self.is_reloading = True

            arcade.schedule(self.reload, 1)

    def reload(self, delta_time):
        if self.is_reloading:
            arcade.play_sound(RELOAD_SOUND)
            self.reload_time -= delta_time
            if self.reload_time <= 0:
                self.ammo = 10  # Refill ammo
                self.is_reloading = False
                arcade.unschedule(self.reload)  # Stop scheduling the reload
        else:
            self.reload_time = 1


class EnemyShoot(arcade.Sprite):
    def __init__(self, image, scale):
        super().__init__(image, scale)

        self.lives = 3

    def check_lives(self, lives):

        if lives == 0:
            self.remove_from_sprite_lists()

    def collision(self, wall_list):
        self.physics_engine_enemy = arcade.PhysicsEngineSimple(self, wall_list)

    def update(self):
        if self.physics_engine_enemy:
            self.physics_engine_enemy.update()


class Grenade(arcade.Sprite):
    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.detonation_time = 3.0  # Час до вибуху 5 секунд


class MyGame(arcade.View):
    def __init__(self):
        super().__init__()
        # Sprites and lists
        self.tile_map = None
        self.wall_list = None
        self.player_sprite = None
        self.player_list = None
        self.scope = None
        self.bullet_list = None
        self.list_of_gems_for_enemies_progress = 0
        self.coin_list = None
        self.enemy_bullet_list = None
        self.grenade_launcher_bullets = None
        self.enemy_list1 = None
        self.lives_list = None
        self.ammo_list = None
        self.enemy_list2 = None
        self.kamikaze_list = None
        self.explosion_list = None
        self.grenade_launchers_list = None
        self.special_list = []
        self.prospector_list = []
        # some useful variables
        self.frame_count = 0
        self.shoot_timer = 0
        self.time_since_last_collision = 0.0
        self.time_between_collision = 1
        # camera initialization
        self.player_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.gui_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    def calculate_distance(self, sprite1, sprite2):
        x1, y1 = sprite1.center_x, sprite1.center_y
        x2, y2 = sprite2.center_x, sprite2.center_y
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def update_distance(self, player_sprite, enemy):
        distance_to_player = self.calculate_distance(enemy, player_sprite)
        if distance_to_player <= enemy.spawn_reinforcement_distance and not enemy.reinforcement_called:
            self.call_reinforcement()
            enemy.reinforcement_called = True


    def call_reinforcement(self):
        for i in range(5):
            enemy_shoot = EnemyShoot('shooter_images/PNG/Soldier 1/soldier1_gun.png', 1.0)
            enemy_shoot.center_x, enemy_shoot.center_y = self.player_sprite.center_x + 200, self.player_sprite.center_y + 30
            self.enemy_list2.append(enemy_shoot)
            self.wall_list.append(enemy_shoot)

    def setup(self):
        self.game_over = False
        self.won = False
        self.background_music = arcade.play_sound(MUSIC)

        self.start_menu = True
        # Player sprite Config
        self.player_sprite = Player('shooter_images/PNG/Hitman 1/hitman1_gun.png', 1, self.player_camera)
        self.player_sprite.center_y = 85
        self.player_sprite.center_x = 85
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)
        # First enemy bullet (will be deleted because it was just research) Fabric patter exists)
        self.bullet_list = arcade.SpriteList()
        # list for collision and other useful actions width sprites
        self.coin_list = arcade.SpriteList()
        self.kamikaze_list = arcade.SpriteList()
        self.enemy_list1 = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()

        self.enemy_list2 = arcade.SpriteList()
        self.lives_list = arcade.SpriteList()
        self.ammo_list = arcade.SpriteList()
        # Fabric pattern first enemy (probably will be optimized
        self.scope = arcade.Sprite('shooter_images/tile_0057.png', 1)
        self.enemy = Enemy('shooter_images/PNG/Zombie 1/zoimbie1_hold.png', 1.0, 5, 1)
        self.enemy.appear(self.player_sprite.center_x + 300, self.player_sprite.center_y + 100)
        self.enemy_list1.append(self.enemy)
        self.explosion_list = arcade.SpriteList()
        self.grenade_launchers_list = arcade.SpriteList()
        self.grenade_launcher_bullets = arcade.SpriteList()


        # map config
        map_name = 'maps/shooter_lvl1.json'
        self.tile_map = arcade.load_tilemap(map_name)
        self.wall_list = self.tile_map.sprite_lists["walls"]
        self.wall_list.append(self.enemy)
        self.roads = self.tile_map.sprite_lists['roads']
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        self.background_layer = self.tile_map.sprite_lists['background']
        self.gems = self.tile_map.sprite_lists['gems']
        # self.ammo_setup()

        self.wall_list = self.tile_map.sprite_lists['walls']
        # useless shit, will be changed
        coin_center_x = 500
        coin_center_y = 300
        i = 0
        while i < 1:
            coin = arcade.Sprite(':resources:images/items/coinGold_ul.png', 0.2)
            coin.center_x = coin_center_x
            coin.center_y = coin_center_y
            self.coin_list.append(coin)
            i += 1
            coin_center_x += 20

        for i in range(self.player_sprite.lives):
            live = arcade.Sprite('shooter_images/PNG/Hitman 1/hitman1_stand.png', 0.6)
            live.center_x = 500 + i * 40  # Зміщення для кожного життя
            live.center_y = 50  # Фіксоване положення по y
            self.lives_list.append(live)
            self.lives_list.draw()


        # end of useless shit
        # arcade game engine config
        self.enemy.collision(self.wall_list)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,  self.wall_list)




    def on_draw(self):
        arcade.start_render()



        self.background_layer.draw()
        self.roads.draw()
        self.wall_list.draw()

        self.player_sprite.update(self.scope.center_x, self.scope.center_y)
        self.player_list.draw()
        self.coin_list.draw()
        self.scope.draw()

        self.bullet_list.draw()

        self.enemy_bullet_list.draw()
        self.enemy_list1.draw()
        self.gems.draw()
        self.enemy_list2.draw()
        self.kamikaze_list.draw()
        self.explosion_list.draw()

        self.grenade_launchers_list.draw()
        self.grenade_launcher_bullets.draw()
        self.gui_camera.use()
        self.lives_list.draw()
        self.player_camera.use()
        #
        # if self.game_over:
        #     arcade.draw_text('Game over, Press E to restart', self.player_sprite.center_x, self.player_sprite.center_y, arcade.color.WHITE, 32)



    def on_key_press(self, symbol: int, modifiers: int):
            if symbol == arcade.key.D:
                self.player_sprite.change_x = MOVEMENT_SPEED
            elif symbol == arcade.key.A:
                self.player_sprite.change_x = -MOVEMENT_SPEED
            elif symbol == arcade.key.W:
                self.player_sprite.change_y = MOVEMENT_SPEED
            elif symbol == arcade.key.S:
                self.player_sprite.change_y = -MOVEMENT_SPEED
            if symbol == arcade.key.E:
                self.setup()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D or symbol == arcade.key.A:
            self.player_sprite.change_x = 0
        elif symbol == arcade.key.W or symbol == arcade.key.S:
            self.player_sprite.change_y = 0

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.scope.center_x = x + self.player_camera.position[0]
        self.scope.center_y = y + self.player_camera.position[1]

    def on_update(self, delta_time: float):
        if not self.lives_list or self.player_sprite.lives <= 0:
            self.game_over = True
        if self.prospector_list:
            for enemy in self.prospector_list:
                if not enemy.reinforcement_called:
                    self.update_distance(self.player_sprite, enemy)







        if self.game_over:
            game_over_view = GameOver(self.player_camera)
            self.window.show_view(game_over_view)
            arcade.stop_sound(self.background_music)
            return
        self.frame_count += 1
        if self.player_sprite.ammo == 0:
            arcade.schedule(self.player_sprite.reload, 2)

        if self.player_sprite.lives <= 0:
                self.game_over = True

        self.time_since_last_collision += delta_time
        if not self.gems and not self.enemy_list1 and not self.enemy_list2:
            self.won = True
            win = Win(self.player_camera)
            self.window.show_view(win)
            arcade.stop_sound(self.background_music)
            return
        player_and_gems_hi_list = arcade.check_for_collision_with_list(self.player_sprite, self.gems)
        if player_and_gems_hi_list:
            for gem in player_and_gems_hi_list:
                self.list_of_gems_for_enemies_progress += 1
                print(self.list_of_gems_for_enemies_progress)
                if self.list_of_gems_for_enemies_progress == 1:
                    new_enemy = Enemy('shooter_images/PNG/Zombie 1/zoimbie1_hold.png', 1.0, 5, 2)
                    new_enemy.appear(self.player_sprite.center_x + 100, self.player_sprite.center_y + 100)
                    new_enemy.collision(self.wall_list)
                    self.enemy_list1.append(new_enemy)
                    self.wall_list.append(new_enemy)

                elif self.list_of_gems_for_enemies_progress == 2:
                    new_enemy = Enemy('shooter_images/PNG/Zombie 1/zoimbie1_hold.png', 1.0, 5, 2)
                    new_enemy.appear(self.player_sprite.center_x + 100, self.player_sprite.center_y + 100)
                    new_enemy.collision(self.wall_list)
                    self.enemy_list1.append(new_enemy)
                    self.wall_list.append(new_enemy)
                    enemy_shoot = EnemyShoot('shooter_images/PNG/Soldier 1/soldier1_gun.png', 1.0)
                    enemy_shoot.center_x, enemy_shoot.center_y = self.player_sprite.center_x + 200, self.player_sprite.center_y + 30
                    self.enemy_list2.append(enemy_shoot)
                    self.wall_list.append(enemy_shoot)

                elif self.list_of_gems_for_enemies_progress == 3:
                    new_enemy = Enemy('shooter_images/PNG/Zombie 1/zoimbie1_hold.png', 1.0, 5, 2)
                    new_enemy.appear(self.player_sprite.center_x + 100, self.player_sprite.center_y + 100)
                    new_enemy.collision(self.wall_list)
                    self.enemy_list1.append(new_enemy)
                    self.wall_list.append(new_enemy)
                    enemy_shoot = EnemyShoot('shooter_images/PNG/Soldier 1/soldier1_gun.png', 1.0)
                    enemy_shoot.center_x, enemy_shoot.center_y = self.player_sprite.center_x + 200, self.player_sprite.center_y + 30
                    self.enemy_list2.append(enemy_shoot)
                    self.wall_list.append(enemy_shoot)
                    kamikaze = Kamikaze('shooter_images/PNG/Robot 1/robot1_hold.png', 1.0, 5, 2)
                    kamikaze.appear(self.player_sprite.center_x + 150, self.player_sprite.center_y + 150)
                    kamikaze.collision(self.wall_list)
                    kamikaze.movement(self.player_sprite, kamikaze.speed, self.lives_list, self.explosion_list)
                    self.kamikaze_list.append(kamikaze)
                    self.wall_list.append(kamikaze)
                elif self.list_of_gems_for_enemies_progress == 4:
                    new_enemy = Enemy('shooter_images/PNG/Zombie 1/zoimbie1_hold.png', 1.0, 5, 2)
                    new_enemy.appear(self.player_sprite.center_x + 100, self.player_sprite.center_y + 100)
                    new_enemy.collision(self.wall_list)
                    self.enemy_list1.append(new_enemy)
                    self.wall_list.append(new_enemy)
                    enemy_shoot = EnemyShoot('shooter_images/PNG/Soldier 1/soldier1_gun.png', 1.0)
                    enemy_shoot.center_x, enemy_shoot.center_y = self.player_sprite.center_x + 200, self.player_sprite.center_y + 30
                    self.enemy_list2.append(enemy_shoot)
                    self.wall_list.append(enemy_shoot)
                    kamikaze = Kamikaze('shooter_images/PNG/Robot 1/robot1_hold.png', 1.0, 5, 2)
                    kamikaze.appear(self.player_sprite.center_x + 150, self.player_sprite.center_y + 150)
                    kamikaze.collision(self.wall_list)
                    kamikaze.movement(self.player_sprite, kamikaze.speed, self.lives_list, self.explosion_list)
                    self.kamikaze_list.append(kamikaze)
                    self.wall_list.append(kamikaze)
                    grenade_launcher = GrenadeLauncher('shooter_images/PNG/Man Brown/manBrown_gun.png', 1.0, 4, 2)
                    grenade_launcher.appear(self.player_sprite.center_x + 250, self.player_sprite.center_y + 250)
                    grenade_launcher.collision(self.wall_list)
                    self.grenade_launchers_list.append(grenade_launcher)
                elif self.list_of_gems_for_enemies_progress == 5:
                    new_enemy = Enemy('shooter_images/PNG/Zombie 1/zoimbie1_hold.png', 1.0, 5, 2)
                    new_enemy.appear(self.player_sprite.center_x + 100, self.player_sprite.center_y + 100)
                    new_enemy.collision(self.wall_list)
                    self.enemy_list1.append(new_enemy)
                    self.wall_list.append(new_enemy)
                    self.special_list.append(new_enemy)
                    print(self.special_list)
                elif self.list_of_gems_for_enemies_progress == 6:
                    prospector = Prospector('shooter_images/PNG/Man Old/manOld_hold.png', 1, 2, 3)
                    prospector.appear(self.player_sprite.center_x + 200, self.player_sprite.center_y + 200)
                    prospector.collision(self.wall_list)
                    prospector.movement(self.player_sprite, prospector.speed)
                    self.enemy_list1.append(prospector)
                    self.wall_list.append(prospector)
                    self.prospector_list.append(prospector)

                else:
                    new_enemy = Enemy('shooter_images/PNG/Zombie 1/zoimbie1_hold.png', 1.0, 5, 2)
                    new_enemy.appear(self.player_sprite.center_x + 100, self.player_sprite.center_y + 100)
                    new_enemy.collision(self.wall_list)
                    self.enemy_list1.append(new_enemy)
                    self.wall_list.append(new_enemy)
                    enemy_shoot = EnemyShoot('shooter_images/PNG/Soldier 1/soldier1_gun.png', 1.0)
                    enemy_shoot.center_x, enemy_shoot.center_y = self.player_sprite.center_x + 200, self.player_sprite.center_y + 30
                    self.enemy_list2.append(enemy_shoot)
                    self.wall_list.append(enemy_shoot)
                    kamikaze = Kamikaze('shooter_images/PNG/Robot 1/robot1_hold.png', 1.0, 5, 2)
                    kamikaze.appear(self.player_sprite.center_x + 150, self.player_sprite.center_y + 150)
                    kamikaze.collision(self.wall_list)
                    kamikaze.movement(self.player_sprite, kamikaze.speed, self.lives_list, self.explosion_list)
                    self.kamikaze_list.append(kamikaze)
                    self.wall_list.append(kamikaze)
                    grenade_launcher = GrenadeLauncher('shooter_images/PNG/Man Brown/manBrown_gun.png', 1.0, 4, 2)
                    grenade_launcher.appear(self.player_sprite.center_x + 250, self.player_sprite.center_y + 250)
                    grenade_launcher.collision(self.wall_list)
                    self.grenade_launchers_list.append(grenade_launcher)
                    new_enemy = Enemy('shooter_images/PNG/Zombie 1/zoimbie1_hold.png', 1.0, 5, 2)
                    new_enemy.appear(self.player_sprite.center_x + 100, self.player_sprite.center_y + 100)
                    new_enemy.collision(self.wall_list)
                    self.enemy_list1.append(new_enemy)
                    self.wall_list.append(new_enemy)
                    self.special_list.append(new_enemy)
                    print(self.special_list)
                    prospector = Prospector('shooter_images/PNG/Man Old/manOld_hold.png', 1, 2, 3)
                    prospector.appear(self.player_sprite.center_x + 200, self.player_sprite.center_y + 200)
                    prospector.collision(self.wall_list)
                    prospector.movement(self.player_sprite, prospector.speed)
                    self.enemy_list1.append(prospector)
                    self.wall_list.append(prospector)
                    self.prospector_list.append(prospector)
                gem.kill()

        # This is logic for enemies who can shoot
        for enemy in self.enemy_list2:

            # First, calculate the angle to the player. We could do this
            # only when the bullet fires, but in this case we will rotate
            # the enemy to face the player each frame, so we'll do this
            # each frame.

            # Position the start at the enemy's current location
            start_x = enemy.center_x
            start_y = enemy.center_y

            # Get the destination location for the bullet
            dest_x = self.player_sprite.center_x
            dest_y = self.player_sprite.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Set the enemy to face the player.
            enemy.angle = math.degrees(angle)
            enemy.collision(self.wall_list)

            # Shoot every 60 frames change of shooting each frame
            if self.frame_count % 60 == 0:
                bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")
                bullet.center_x = start_x
                bullet.center_y = start_y

                # Angle the bullet sprite
                bullet.angle = math.degrees(angle)

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                bullet.change_x = math.cos(angle) * BULLET_SPEED
                bullet.change_y = math.sin(angle) * BULLET_SPEED

                self.enemy_bullet_list.append(bullet)

        #  logic for grenade launchers
        for enemy in self.grenade_launchers_list:

            start_x = enemy.center_x
            start_y = enemy.center_y

            # Get the destination location for the bullet
            dest_x = self.player_sprite.center_x
            dest_y = self.player_sprite.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Set the enemy to face the player.
            enemy.angle = math.degrees(angle)


            # Shoot every 60 frames change of shooting each frame
            if self.frame_count % 60 == 0:
                bullet = Grenade("shooter_images/pixel_grenade.png", 1.0)
                bullet.center_x = start_x
                bullet.center_y = start_y

                # Angle the bullet sprite
                bullet.angle = math.degrees(angle)

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                bullet.change_x = math.cos(angle) * 6
                bullet.change_y = math.sin(angle) * 6

                self.grenade_launcher_bullets.append(bullet)



        for enemy in self.kamikaze_list:
            enemy.update()
            enemy.movement(self.player_sprite, self.enemy.speed, self.lives_list, self.explosion_list)



        for enemy in self.enemy_list1:
            enemy.update()
        enemy_and_player_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list1)
        if enemy_and_player_hit_list:
            if self.lives_list and self.time_since_last_collision >= self.time_between_collision:
                self.time_since_last_collision = 0
                arcade.play_sound(HURT_PLAYER_SOUND)

                if enemy.damage > self.player_sprite.lives:

                    self.game_over = True
                    return
                self.player_sprite.lives -= self.enemy.damage

                for i in range(enemy.damage):

                    self.lives_list.pop(0)



                  # Увімкніть прапор, щоб уникнути повторних зменшень життів

        # Ваші інші оновлення
         # Скидання пра

        for bullet in self.bullet_list:
            bullet_hit_width_enemies = arcade.check_for_collision_with_list(bullet, self.enemy_list1)
            bullet_and_walls_hit_list = arcade.check_for_collision_with_list(bullet, self.wall_list)
            bullet_hit_width_enemies_shoot = arcade.check_for_collision_with_list(bullet, self.enemy_list2)
            hit_list_with_player_bullet_kamikaze = arcade.check_for_collision_with_list(bullet, self.kamikaze_list)
            bullet_hit_with_grenade_launcher = arcade.check_for_collision_with_list(bullet, self.grenade_launchers_list)
            if hit_list_with_player_bullet_kamikaze:
                for enemy in hit_list_with_player_bullet_kamikaze:
                    arcade.play_sound(ENEMY_HURT_SOUND)
                    enemy.health -= 1
            if bullet_hit_width_enemies_shoot:
                arcade.play_sound(ENEMY_HURT_SOUND)
                bullet.remove_from_sprite_lists()
                for enemy in bullet_hit_width_enemies_shoot:
                    enemy.lives -= 1
                    enemy.check_lives(enemy.lives)
            if bullet_hit_width_enemies:
                arcade.play_sound(ENEMY_HURT_SOUND)
                bullet.remove_from_sprite_lists()
                for enemy in bullet_hit_width_enemies:  # Ітеруємо лише по тих ворогах, з якими була колізія
                    enemy.health -= 1
                    if enemy.health == 0:
                        if enemy in self.special_list:
                            for i in range(5):
                                new_enemy = Enemy('shooter_images/PNG/Zombie 1/zoimbie1_hold.png', 0.6, 5, 2)
                                new_enemy.appear(self.player_sprite.center_x + 100, self.player_sprite.center_y + 100)
                                new_enemy.collision(self.wall_list)
                                self.enemy_list1.append(new_enemy)
                                self.wall_list.append(new_enemy)

                        enemy.die()



            if bullet_hit_with_grenade_launcher:
                arcade.play_sound(ENEMY_HURT_SOUND)
                bullet.remove_from_sprite_lists()
                for enemy in bullet_hit_with_grenade_launcher:
                    enemy.health -= 1
                    if enemy.health <= 0:
                        enemy.die()
            if bullet_and_walls_hit_list:
                bullet.remove_from_sprite_lists()
        for bullet in self.grenade_launcher_bullets:
            bullet.detonation_time -= 1 / 60  # Зменшуємо час до вибуху на 1/60 секунди

            if bullet.detonation_time <= 0:
                explosion = Explosion(bullet.center_x, bullet.center_y)
                self.explosion_list.append(explosion)
                arcade.play_sound(EXPLOSION_SOUND)
                bullet.remove_from_sprite_lists()
        # grenade launcher bullets collision
        for grenade in self.grenade_launcher_bullets:
            if grenade.collides_with_sprite(self.player_sprite):
                explosion = Explosion(grenade.center_x, grenade.center_y)
                self.explosion_list.append(explosion)
                arcade.play_sound(EXPLOSION_SOUND)
                grenade.remove_from_sprite_lists()
                self.player_sprite.lives -= 3
                for i in range(4):
                    if not self.lives_list:
                        self.game_over = True
                        return
                    self.lives_list.pop(0)


        for enemy in self.enemy_list1:
            dest_x = self.player_sprite.center_x
            dest_y = self.player_sprite.center_y

            x_diff = dest_x - enemy.center_x
            y_diff = dest_y - enemy.center_y
            angle = math.atan2(y_diff, x_diff)

            # Встановлення кута спрайта ворога
            enemy.angle = math.degrees(angle)
            enemy.movement(self.player_sprite, self.enemy.speed)



        player_coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        if player_coin_hit_list:
            for coin in player_coin_hit_list:
                coin.remove_from_sprite_lists()
                arcade.play_sound(COIN_SOUND)
                arcade.play_sound(ENEMY_SOUND)
                for i in range(random.randrange(0, 5)):
                    new_enemy = Enemy('shooter_images/PNG/Zombie 1/zoimbie1_hold.png', 1.0, 5, 1)
                    new_enemy.appear(self.player_sprite.center_x + i * 40, self.player_sprite.center_y + 100)
                    new_enemy.collision(self.wall_list)
        enemy_shoot_bullet_and_player_collision = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_bullet_list)
        if enemy_shoot_bullet_and_player_collision:
            for bullet in enemy_shoot_bullet_and_player_collision:
                bullet.remove_from_sprite_lists()
                self.player_sprite.lives -= 1
                self.lives_list.pop(0)





        self.bullet_list.update()
        self.physics_engine.update()
        self.bullet_list.update()
        self.scroll_to_player()
        self.coin_list.update()
        self.enemy_list1.update()
        self.enemy_list2.update()
        self.kamikaze_list.update()
        self.explosion_list.update()
        self.enemy_bullet_list.update()
        self.grenade_launchers_list.update()
        self.grenade_launcher_bullets.update()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.player_sprite.ammo > 0:
            # Shooting logic
            self.player_sprite.shoot(x, y, self.bullet_list, PISTOL_SHOOT_SOUND)
        else:
            # Ammo is zero, start reloading

            self.player_sprite.is_reloading = True
            arcade.schedule(self.player_sprite.reload, 1)


    def scroll_to_player(self):
        """
        Scroll the window to the player.
        """
        position = Vec2(self.player_sprite.center_x - self.window.width / 2,
                        self.player_sprite.center_y - self.window.height / 2)
        self.player_camera.move_to(position, CAMERA_SPEED)

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.player_camera.resize(int(width), int(height))
        self.gui_camera.resize(int(width), int(height))


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "My Game with Menu")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
