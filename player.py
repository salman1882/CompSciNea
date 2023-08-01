import pygame
from settings import TILE_SIZE

class Player:
    def __init__(self, x, y, speed, width, height):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height

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

    def draw(self, screen):
        pygame.draw.rect(screen, (255), pygame.Rect(self.x, self.y, self.width, self.height))

    def collides_with(self, other_rect):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return player_rect.colliderect(other_rect)