
import pygame
from player import Projectile

class Fireball(Projectile):
    def __init__(self, x, y, direction, speed=10, damage=10):
        super().__init__(x, y, direction, speed)
        self.damage = damage

    
    def update(self):
        super().update()
        
        


        
