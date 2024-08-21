import arcade
from abc import ABC, abstractmethod
import math
import random
BULLET_SPEED = 5
KAMIKAZE_SOUND = arcade.load_sound('sound/explosion.wav')
class Explosion(arcade.AnimatedTimeBasedSprite):
    def __init__(self, position_x, position_y):
        super().__init__()

        # Завантажуємо всі кадри вибуху
        for i in range(1, 5):  # Залежить від кількості кадрів
            texture = arcade.load_texture(f"explosion_frames/explosion{i}.png")
            frame = arcade.AnimationKeyframe(i, 60, texture)  # 60 - тривалість кадру в мс
            self.frames.append(frame)

        # Встановлюємо початкове положення вибуху
        self.center_x = position_x
        self.center_y = position_y

    def update(self):
        # Оновлюємо анімацію
        super().update_animation()

        # Якщо поточний індекс кадру досягнув кінця списку кадрів, завершити анімацію
        if self.cur_frame_idx >= len(self.frames) - 1:
            self.remove_from_sprite_lists()


class Enemy(arcade.Sprite):
    def __init__(self, image_path, scale, health, speed):
        super().__init__(image_path, scale)
        self.health = health
        self.damage = 2
        self.speed = speed
        self.physics_engine_enemy = None

    def die(self):
        self.remove_from_sprite_lists()

    def attack(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def appear(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y

    def movement(self, player_sprite, enemy_speed):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Random 1 in 100 chance that we'll change from our old direction and
        # then re-aim toward the player
        if random.randrange(100) == 0:
            start_x = self.center_x
            start_y = self.center_y

            # Get the destination location for the bullet
            dest_x = player_sprite.center_x
            dest_y = player_sprite.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            self.change_x = math.cos(angle) * enemy_speed
            self.change_y = math.sin(angle) * enemy_speed

    def collision(self, wall_list):
        self.physics_engine_enemy = arcade.PhysicsEngineSimple(self, wall_list)

    def update(self):
        if self.physics_engine_enemy:
            self.physics_engine_enemy.update()



class Kamikaze(arcade.Sprite):
    def __init__(self, image_path, scale,  health, speed):
        super().__init__(image_path, scale)
        self.physics_engine_enemy = None
        self.health = health
        self.speed = speed
        self.damage = 5

    def attack(self, damage):
        pass

    def appear(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y

    def die(self, explosion_list):
        # Створюємо вибух
        explosion = Explosion(self.center_x, self.center_y)
        explosion_list.append(explosion)

        # Видаляємо Kamikaze
        self.remove_from_sprite_lists()

    def movement(self, player_sprite, enemy_speed, lives_list, explosion_list):
        if self.health <= 0:
            self.die(explosion_list)
        if self.collides_with_sprite(player_sprite):
            arcade.play_sound(KAMIKAZE_SOUND)
            player_sprite.lives -= self.damage
            for i in range(self.damage):
                if not lives_list:
                    return
                lives_list.pop(0)

            self.die(explosion_list)

        start_x = self.center_x
        start_y = self.center_y

        # Get the destination location for the bullet
        dest_x = player_sprite.center_x
        dest_y = player_sprite.center_y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        self.change_x = math.cos(angle) * enemy_speed
        self.change_y = math.sin(angle) * enemy_speed
        self.angle = math.degrees(angle)
    def collision(self, wall_list):
        self.physics_engine_enemy = arcade.PhysicsEngineSimple(self, wall_list)

    def update(self):
        if self.physics_engine_enemy:
            self.physics_engine_enemy.update()


class GrenadeLauncher(arcade.Sprite):
    def __init__(self, image_path, scale,  health, speed):
        super().__init__(image_path, scale)
        self.physics_engine_enemy = None
        self.health = health
        self.speed = speed
        self.damage = 5


    def attack(self, damage):
        pass

    def appear(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y

    def die(self):
        # Видаляємо Kamikaze
        self.remove_from_sprite_lists()

    def movement(self, player_sprite, enemy_speed, lives_list, explosion_list):
       pass

    def collision(self, wall_list):
        self.physics_engine_enemy = arcade.PhysicsEngineSimple(self, wall_list)

    def update(self):
        if self.physics_engine_enemy:
            self.physics_engine_enemy.update()


class Prospector(arcade.Sprite):
    def __init__(self, image_path, scale, health, speed):
        super().__init__(image_path, scale)
        self.health = health
        self.damage = 2
        self.speed = speed
        self.physics_engine_enemy = None
        self.spawn_reinforcement_distance = 50
        self.reinforcement_called = False

    def die(self):
        self.remove_from_sprite_lists()

    def attack(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def appear(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y



    def movement(self, player_sprite, enemy_speed):
        start_x = self.center_x
        start_y = self.center_y

        # Get the destination location for the bullet
        dest_x = player_sprite.center_x
        dest_y = player_sprite.center_y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        self.change_x = math.cos(angle) * enemy_speed
        self.change_y = math.sin(angle) * enemy_speed
        self.angle = math.degrees(angle)



    def collision(self, wall_list):
        self.physics_engine_enemy = arcade.PhysicsEngineSimple(self, wall_list)

    def update(self):
        if self.physics_engine_enemy:
            self.physics_engine_enemy.update()