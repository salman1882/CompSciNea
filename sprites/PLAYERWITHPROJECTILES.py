import pygame
from settings import TILE_SIZE

class Player:
    attack_cooldown = 300

    def __init__(self, x, y, speed, width, height):
        self.health = 3
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.hitbox_width_offset = 20  # Additional width for the hitbox
        self.hitbox_height_offset = 20  # Additional height for the hitbox
        self.direction = 'right'
        self.is_attacking = False
        self.attack_start_time = None
        self.animation_cooldown = 80
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.sword_width = 20  # Width of the sword's hitbox
        self.sword_height = 20  # Height of the sword's hitbox
        self.sword_rect = pygame.Rect(self.x, self.y, self.sword_width, self.sword_height)  # Initial sword rectangle
        self.last_hit_time = 0  # Time of the last hit by an enemy
        self.weapon_type = 'sword'  # Current weapon type ('sword' or 'fists')
        self.projectiles = []  # List to store projectiles when using fists

    def handle_movement(self, keys, walls):
        if self.is_attacking:
            return

        if keys[pygame.K_SPACE] and not self.is_attacking:
            self.update_sword_and_projectiles()  # Update the sword's rectangle during an attack
            self.is_attacking = True
            self.attack_start_time = pygame.time.get_ticks()

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
        new_rect = pygame.Rect(new_x + (64 - self.width) // 2, new_y + (100 - self.height) // 2, self.width, self.height)

        if dx > 0: self.direction = 'right'
        elif dx < 0: self.direction = 'left'
        elif dy > 0: self.direction = 'down'
        elif dy < 0: self.direction = 'up'

        collision = False
        for i in walls:
            if new_rect.colliderect(i):
                collision = True
                break

        if not collision:
            self.x = new_x
            self.y = new_y

    def draw(self, screen):
        pygame.draw.rect(screen, (255), pygame.Rect(self.x, self.y, self.width, self.height))

    def collides_with(self, other_rect):
        player_rect = pygame.Rect(self.x, self.y, self.width + self.hitbox_width_offset, self.height + self.hitbox_height_offset)
        return player_rect.colliderect(other_rect)

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame = self.frame + 1 
            self.last_update = current_time
            if self.frame >= 8:
                self.frame = 0

    def update_rect(self):
        hitbox_width = self.width + self.hitbox_width_offset
        hitbox_height = self.height + self.hitbox_height_offset
        self.rect = pygame.Rect(self.x, self.y, hitbox_width, hitbox_height)

    def handle_collisions(self, enemies, walls):
       self.update_rect()
       current_time = pygame.time.get_ticks()
       if current_time - self.last_hit_time < 1000:
           return
       for enemy in enemies:
           enemy.update_rect()
           if self.rect.colliderect(enemy.rect):
             self.last_hit_time = current_time
             self.health -= 1
             knockback_distance = 100
            
             # Calculate the vector from the enemy to the player
             dx = self.x - enemy.x
             dy = self.y - enemy.y
            
             # Normalize the vector
             distance = (dx**2 + dy**2)**0.5
             dx /= distance
             dy /= distance
            
             # Calculate new position for knockback
             new_x = self.x + dx * knockback_distance
             new_y = self.y + dy * knockback_distance
             new_rect = pygame.Rect(new_x + (64 - self.width) // 2, new_y + (100 - self.height) // 2, self.width, self.height)

             # Check if new position collides with walls
             collision = False
             for wall in walls:
                 if new_rect.colliderect(wall):
                     collision = True

             # Apply knockback if no collision with walls
             if not collision:
                 self.x = new_x
                 self.y = new_y

             # Apply knockback to the enemy in the opposite direction
             enemy.x -= dx * knockback_distance
             enemy.y -= dy * knockback_distance

    def get_sword_offset(self):
        offset_x = 0
        offset_y = 0
        if self.direction == 'right':
            offset_x = 45
            offset_y = 45
        elif self.direction == 'left':
            offset_x = -45
            offset_y = 45
        elif self.direction == 'up':
            offset_x = 35
            offset_y = -50
        elif self.direction == 'down':
            offset_x = 31
            offset_y = 70
        return offset_x, offset_y
        
    
    def update_sword_and_projectiles(self):
        if self.weapon_type == 'sword':
            offset_x, offset_y = self.get_sword_offset()
            self.sword_rect.x = self.x + offset_x
            self.sword_rect.y = self.y + offset_y
        elif self.weapon_type == 'fists':
            # Create a projectile when attacking with fists
            projectile = self.create_projectile()
            self.projectiles.append(projectile)
    
        offset_x, offset_y = self.get_sword_offset()
        self.sword_rect.x = self.x + offset_x
        self.sword_rect.y = self.y + offset_y
        return offset_x, offset_y

    
    def check_weapon_collisions(self, enemies):
        if not self.is_attacking: 
            return 

        if self.weapon_type == 'sword':
            for enemy in enemies:
                # Check for collisions with the sword's rectangle
                if self.sword_rect.colliderect(enemy.rect):
                    enemy.health -= 1
                    if enemy.health <= 0:
                        enemy.active_enemies.remove(enemy)
        elif self.weapon_type == 'fists':
            for projectile in self.projectiles:
                for enemy in enemies:
                    # Check for collisions with projectiles
                    projectile_rect = pygame.Rect(*projectile['position'], 10, 10) # Example projectile size
                    if projectile_rect.colliderect(enemy.rect):
                        enemy.health -= 1
                        if enemy.health <= 0:
                            enemy.active_enemies.remove(enemy)
    
        if self.is_attacking == False: 
            return 
        for enemy in enemies:
            # Check for collisions with the sword's rectangle
            if self.sword_rect.colliderect(enemy.rect):
                enemy.health -=  1 
                if enemy.health <= 0:
                    enemy.active_enemies.remove(enemy)

        
    def draw_health(self, screen, SCREEN_WIDTH):
        square_size = 20
        spacing = 5
        top_right_x = SCREEN_WIDTH - (3 * square_size + 2 * spacing)
        top_right_y = 10

        for i in range(3):
            color = pygame.Color('black') if i >= self.health else pygame.Color('red')
            pygame.draw.rect(screen, color, (top_right_x + i * (square_size + spacing), top_right_y, square_size, square_size))

    def switch_weapon(self):
        # Toggle between 'sword' and 'fists'
        if self.weapon_type == 'sword':
            self.weapon_type = 'fists'
        else:
            self.weapon_type = 'sword'

    def create_projectile(self):
        # Create a projectile based on the player's direction and position
 
        projectile_speed = 10
        projectile_direction = self.direction
        projectile_position = (self.x, self.y)
        return {'speed': projectile_speed, 'direction': projectile_direction, 'position': projectile_position}

    def update_projectiles(self, walls):
        # Update the position of each projectile based on its direction
        for projectile in self.projectiles:
            dx, dy = 0, 0
            if projectile['direction'] == 'right':
                dx = projectile['speed']
            elif projectile['direction'] == 'left':
                dx = -projectile['speed']
            elif projectile['direction'] == 'up':
                dy = -projectile['speed']
            elif projectile['direction'] == 'down':
                dy = projectile['speed']
            
            projectile['position'] = (projectile['position'][0] + dx, projectile['position'][1] + dy)
            
            # Check for collisions with walls or boundaries
            projectile_rect = pygame.Rect(*projectile['position'], 10, 10) # Example projectile size
            for wall in walls:
                if projectile_rect.colliderect(wall):
                    self.projectiles.remove(projectile)
                    break

    def handle_projectiles(self, enemies, walls):
        # Iterate through the projectiles and update their positions
        for projectile in self.projectiles:
            # Calculate the new position based on the direction and speed
            dx, dy = 0, 0
            if projectile['direction'] == 'right':
                dx = projectile['speed']
            elif projectile['direction'] == 'left':
                dx = -projectile['speed']
            elif projectile['direction'] == 'up':
                dy = -projectile['speed']
            elif projectile['direction'] == 'down':
                dy = projectile['speed']
            projectile['position'] = (projectile['position'][0] + dx, projectile['position'][1] + dy)

            # Check for collisions with enemies
            projectile_rect = pygame.Rect(*projectile['position'], 10, 10) # Example projectile size
            for enemy in enemies:
                if projectile_rect.colliderect(enemy.rect):
                    enemy.health -= 1
                    if enemy.health <= 0:
                        enemy.active_enemies.remove(enemy)
                    # Remove the projectile after a collision
                    self.projectiles.remove(projectile)
                    break

            # Check for collisions with walls or other objects (if needed)
            # ...

        # Remove projectiles that are out of bounds (if needed)
        # ...
