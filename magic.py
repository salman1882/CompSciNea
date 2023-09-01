import pygame
from projectile import Projectile
from enemy import Enemy

class Fireball(Projectile):

    last_fireball_time = 0

    def __init__(self, x, y, direction, speed=10, damage=10, max_travel_distance=480):
        super().__init__(x, y, direction, speed)
        self.damage = damage
        self.image = pygame.image.load('sprites/fireball.png')  # Load the fireball image
        self.radius = 10  
        self.max_radius = 250
        self.growth_rate = 1.5
        self.distance_traveled = 0
        self.growth_start_distance = 479
        self.max_size_duration = 0
        self.max_travel_distance = max_travel_distance
        self.time_counter = 0
        self.lifetime_frames = 350 # 60 x lifetime in seconds
        self.rotation = 0

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
        scaled_image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
        camera.draw_with_offset(screen, scaled_image, (self.x - self.radius, self.y - self.radius))

    def get_hitbox(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
