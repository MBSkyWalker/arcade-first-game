import arcade
from abc import ABC, abstractmethod
import math
import random

class AbstractEnemy(ABC):
    @abstractmethod
    def attack(self, damage):
        pass

    @abstractmethod
    def die(self):
        pass
    @abstractmethod
    def movement(self, player_sprite, enemy_speed):
        pass

    @abstractmethod
    def appear(self, center_x, center_y):
        pass



class Enemy(arcade.Sprite, AbstractEnemy):
    def __init__(self, image_path, scale, health, damage, speed):
        super().__init__(image_path, scale)
        self.health = health
        self.damage = damage
        self.speed = speed

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




