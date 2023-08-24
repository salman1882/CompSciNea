import pygame
import random
from player import Player
from camera import Camera
from settings import TILE_SIZE  
from settings import MAP    

class Enemy(Player):
    # Class variable to store all active enemies
    active_enemies = []

    def __init__(self, x, y, width, height, speed=1, image=pygame.image.load('sprites/ghost.png')):
        super().__init__(x, y, width, height,speed)
        self.direction = 'left'  # Initial direction enemy is facing.
        self.image = image  # Image for the enemy
        self.health = 3
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
        dx /= distance
        dy /= distance
        
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

