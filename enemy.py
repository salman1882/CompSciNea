import pygame
import random
from player import Player
from camera import Camera
from settings import TILE_SIZE  
from settings import MAP    

class Enemy(Player):
    # Class variable to store all active enemies
    active_enemies = []

    def __init__(self, x, y, speed, width, height, image=pygame.image.load('sprites/ghost.png')):
        super().__init__(x, y, speed, width, height)
        self.direction = 'left'  # Initial direction enemy is facing. Set to 'left' for differentiation.
        self.image = image  # Image for the enemy
        Enemy.active_enemies.append(self)  # Add the enemy to the active enemies list

    # Override the draw method to render the enemy image
    def draw(self, screen, camera):
        if self.image:
            camera.draw_with_offset(screen, self.image, (self.x, self.y))
        else:
            adjusted_rect = camera.apply_offset(pygame.Rect(self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, (255, 0, 0), adjusted_rect)  # Draw a red placeholder rectangle if no image

    
    def spawn_enemies(last_spawn_time):
        MAP_WIDTH = len(MAP[0])
        MAP_HEIGHT = len(MAP)
        
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time >= 5000 and len(Enemy.active_enemies) < 5: 
            
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
            return current_time  # Update the last spawn time
        return last_spawn_time

        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time >= 5000 and len(Enemy.active_enemies) < 5: 
            x = random.randint(0, screen_width - TILE_SIZE)
            y = random.randint(0, screen_height - TILE_SIZE)
            enemy = Enemy(x, y, 5, TILE_SIZE, TILE_SIZE)  
            return current_time  # Update the last spawn time
        return last_spawn_time
