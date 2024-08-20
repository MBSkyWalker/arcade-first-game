import arcade
from abc import ABC, abstractmethod
import math
import random

class AbstractEnemy(ABC):
    @abstractmethod
    def attack(self, damage):
        pass

    @abstractmethod
    def die(self, enemy_list):
        pass
    @abstractmethod
    def movement(self, player_sprite):
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

    def movement(self, player_sprite):
        if random.randrange(100) == 0:
            x_diff = player_sprite.center_x - self.center_x
            y_diff = player_sprite.center_y - self.center_y
            angle = math.atan2(y_diff, x_diff)
            self.change_x = math.cos(angle) * self.speed
            self.change_y = math.sin(angle) * self.speed

        self.center_x += self.change_x
        self.center_y += self.change_y



