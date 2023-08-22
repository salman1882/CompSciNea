import pygame
from settings import TILE_SIZE

class Player:
    def __init__(self, x, y, speed, width, height, spritesheet):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.spritesheet = spritesheet
        self.image = self.spritesheet.get_image(0, self.width, self.height, 1, (0,0,0))
        self.frame = 0
        self.direction = 'right'

    def move(self, dx, dy, walls):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        new_rect = pygame.Rect(new_x, new_y, self.width, self.height)

        # Check for collisions
        for i in walls:
            if new_rect.colliderect(i):
                return  

        # If there are no collisions update pos
        self.x = new_x
        self.y = new_y

        # Update direction
        if dx > 0:
            self.direction = 'right'
        elif dx < 0:
            self.direction = 'left'
        elif dy > 0:
            self.direction = 'down'
        elif dy < 0:
            self.direction = 'up'
        
        # Update frame
        self.frame = (self.frame + 1) % 8

        # Update image
        if self.direction == 'right':
            self.image = self.spritesheet.get_image(self.frame, self.width, self.height, 1, (0,0,0))
        elif self.direction == 'down':
            self.image = self.spritesheet.get_image(self.frame + 8, self.width, self.height, 1, (0,0,0))
        elif self.direction == 'left':
            self.image = self.spritesheet.get_image(self.frame + 16, self.width, self.height, 1, (0,0,0))
        elif self.direction == 'up':
            self.image = self.spritesheet.get_image(self.frame + 24, self.width, self.height, 1, (0,0,0))

        print(f"Direction: {self.direction}, Frame: {self.frame}")

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def collides_with(self, other_rect):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return player_rect.colliderect(other_rect)