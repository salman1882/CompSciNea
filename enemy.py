import pygame
import random
from player import Player
from camera import Camera
from settings import TILE_SIZE  
from settings import *  

class Enemy(Player):
    # Class variable to store all active enemies
    active_enemies = []
    current_wave = 1  # Tracks the current wave number
    enemies_in_current_wave = 0  # Tracks the number of enemies spawned in the current wave

    def __init__(self, x, y, width, height, speed=1, image=pygame.image.load('sprites/ghost.png')):
        super().__init__(x, y, width, height,speed)
        self.direction = 'left'  # Initial direction enemy is facing.
        self.image = image  # Image for the enemy
        self.health = 30
        self.update_rect()  # Initialize the enemy's rectangle
        Enemy.active_enemies.append(self)  # Add the enemy to the active enemies list

    def check_collision(self, new_rect, walls):
        for wall in walls:
            if new_rect.colliderect(wall):
                return True
        return False

    def move_towards_player(self, player, walls):
        # Calculate the vector from enemy to player
        dx = player.x - self.x
        dy = player.y - self.y
        
        # Calculate the distance between the enemy and player
        distance = (dx**2 + dy**2)**0.5
        
        # If the player is close enough to the enemy, stop moving
        if distance < 55:
            return
        
        # Normalize the vector
        dx = dx / distance
        dy = dy / distance
        
        # Adjust the movement by the enemy's speed
        move_dx = self.speed * dx
        move_dy = self.speed * dy
        
        # Check for potential collisions in x direction
        new_rect_x = pygame.Rect(self.x + move_dx, self.y, self.width, self.height)
        if not self.check_collision(new_rect_x, walls):
            self.x += move_dx

        # Check for potential collisions in y direction
        new_rect_y = pygame.Rect(self.x, self.y + move_dy, self.width, self.height)
        if not self.check_collision(new_rect_y, walls):
            self.y += move_dy

    def slide (self, walls):
        # Adjust the enemy's position if it collides with any walls
        for wall in walls:
            while self.rect.colliderect(wall):
                if self.vx > 0:  # Moving right; Hit the left side of the wall
                    self.x -= 1
                if self.vx < 0:  # Moving left; Hit the right side of the wall
                    self.x += 1
                if self.vy > 0:  # Moving down; Hit the top side of the wall
                    self.y -= 1
                if self.vy < 0:  # Moving up; Hit the bottom side of the wall
                    self.y += 1
                self.update_rect()

    # Override the draw method to render the enemy image
    def draw(self, screen, camera):
        if self.image:
            camera.draw_with_offset(screen, self.image, (self.x, self.y))
        else:
            adjusted_rect = camera.apply_offset(pygame.Rect(self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, (255, 0, 0), adjusted_rect)  

    
    def spawn_enemies(last_spawn_time):
        base_enemies = 5
        growth_rate = 1.5
        max_enemies_for_wave = round(base_enemies * (growth_rate ** (Enemy.current_wave - 1)))
        MAP_WIDTH = len(MAP[0])
        MAP_HEIGHT = len(MAP)
        
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time >= 4000 and Enemy.enemies_in_current_wave < max_enemies_for_wave: 
            
            # Ensure the enemy spawns in a valid position
            valid_spawn = False
            while not valid_spawn:
                x_tile = random.randint(0, MAP_WIDTH - 1)
                y_tile = random.randint(0, MAP_HEIGHT - 1)
                
                if MAP[y_tile][x_tile] == ' ':
                    valid_spawn = True
            
            x = x_tile * TILE_SIZE
            y = y_tile * TILE_SIZE
            
            enemy = Enemy(x, y, 5, TILE_SIZE, TILE_SIZE)  
            Enemy.enemies_in_current_wave += 1
            return current_time  # Update the last spawn time
        # Transition to the next wave if all enemies of the current wave are defeated
        if not Enemy.active_enemies and Enemy.enemies_in_current_wave >= max_enemies_for_wave:
            Enemy.current_wave += 1  # Move to the next wave
            Enemy.enemies_in_current_wave = 0  # Reset the count for the new wave
        return last_spawn_time
    def display_wave_number(screen, font):
    
      # Render and display the current wave number at the top middle of the screen
       wave_surface = font.render(f"Wave: {Enemy.current_wave}", True, pygame.Color('white'))
       wave_position = (SCREEN_WIDTH // 2 - wave_surface.get_width() // 2, 10)
       screen.blit(wave_surface, wave_position)

