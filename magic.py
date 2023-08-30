
import pygame
from projectile import Projectile
from enemy import Enemy

class Fireball(Projectile):

    last_fireball_time = 0
    def __init__(self, x, y, direction, speed=10, damage=10, max_travel_distance=600):
        super().__init__(x, y, direction, speed)
        self.damage = damage
        self.radius = 10  # Initial radius of the fireball
        self.max_radius = 250  # Maximum size the fireball can grow t
        self.growth_rate = 1.5  # Amount by which the fireball grows each update
        self.distance_traveled = 0  # Distance the fireball has traveled
        self.growth_start_distance = 599  # Distance after which the fireball starts growing
        self.max_size_duration = 0  # Time the fireball has been at its maximum size
        self.max_travel_distance = max_travel_distance
        self.time_counter = 0  # Frame counter for the Fireball
        self.lifetime_frames = 311  # (Time x 60 (amount of frames))


    def update(self):
        # Update the fireball's position only if it hasn't traveled its maximum distance
        if self.distance_traveled < self.max_travel_distance:
            super().update()
            self.distance_traveled += self.speed  # Update the distance traveled
        
        # If the fireball has traveled beyond the growth_start_distance, start growing
        if self.distance_traveled > self.growth_start_distance and self.radius < self.max_radius:
            self.radius += self.growth_rate
        
        # If the fireball is at its maximum size, start the timer
        if self.radius >= self.max_radius:
            self.max_size_duration += 16
        
        
        self.time_counter += 1  # Increment the counter for each frame
        if self.time_counter > self.lifetime_frames:
            self.remove = True

    def render(self, screen, camera):
        fireball_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(fireball_surface, (255, 0, 0), (self.radius, self.radius), self.radius)
        camera.draw_with_offset(screen, fireball_surface, (self.x - self.radius, self.y - self.radius))
    
    def get_hitbox(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
