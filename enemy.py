
import pygame
from player import Player

class Enemy(Player):
    def __init__(self, x, y, speed, width, height, image=None):
        super().__init__(x, y, speed, width, height)
        self.direction = 'left'  
        self.image = image  

    # DEAl with movement later
    def handle_movement(self):
        pass

    # Override the draw method to render the enemy image
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
