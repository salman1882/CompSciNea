
import pygame
from settings import TILE_SIZE

# Define the Player class
class Player:
    # Set a constant for attack cooldown time (in milliseconds)
    attack_cooldown = 300

    def __init__(self, x, y, speed, width, height):
        self.x = x  
        self.y = y  
        self.speed = speed 
        self.width = width  
        self.height = height  
        self.direction = 'right'  # Initial direction player is facing
        self.is_attacking = False 
        self.attack_start_time = None  
        self.animation_cooldown = 80  # Time between animation frames
        self.frame = 0 
        self.last_update = pygame.time.get_ticks() 

    def handle_movement(self, keys, walls):
        # If the player is attacking, ignore movement keys
        if self.is_attacking:
            return
        
        # Check for spacebar press to trigger attack state
        if keys[pygame.K_SPACE] and not self.is_attacking:
            self.is_attacking = True
            self.attack_start_time = pygame.time.get_ticks()

        # Handle movement keys
        if keys[pygame.K_a]:
            self.move(-10, 0, walls)
        if keys[pygame.K_d]:
            self.move(10, 0, walls)
        if keys[pygame.K_w]:
            self.move(0, -10, walls)
        if keys[pygame.K_s]:
            self.move(0, 10, walls)

    def move(self, dx, dy, walls):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Define a new rectangle for the player's intended position
        new_rect = pygame.Rect(new_x + (64 - self.width) // 2, new_y + (100 - self.height) // 2, self.width, self.height)

        # Update the player's direction based on the movement deltas
        if dx > 0: self.direction = 'right'
        elif dx < 0: self.direction = 'left'
        elif dy > 0: self.direction = 'down'
        elif dy < 0: self.direction = 'up'

        # Check for collisions with walls
        collision = False
        for i in walls:
            if new_rect.colliderect(i):
                collision = True
                break

        # If there are no collisions, update the player's position
        if not collision:
            self.x = new_x
            self.y = new_y

    def draw(self, screen):
        pygame.draw.rect(screen, (255), pygame.Rect(self.x, self.y, self.width, self.height))

    def collides_with(self, other_rect):
        # Check if the player collides with another rectangle
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return player_rect.colliderect(other_rect)

    def update_animation(self):
        # Update the player's animation frame
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame = self.frame + 1 
            self.last_update = current_time
            # Reset the frame to 0 after reaching the final frame of the animation
            if self.frame >= 8:
                self.frame = 0
