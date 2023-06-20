import pygame
from settings import TILE_SIZE

class Player:
    def __init__(self, x, y, speed, width, height):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255), pygame.Rect(self.x, self.y, self.width, self.height))

    def collides_with(self, other_rect):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return player_rect.colliderect(other_rect)