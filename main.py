from enemy import Enemy
import pygame
import spritesheet
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, MAP
from player import *
from magic import Fireball
from title_screen import TitleScreen

#IMPORTANT, fix sprite continous running and movement speed higher on diag, cooldown between attacks, enemeis kb doesnt work well, if even amount of enemies are on player than no kb taken, kb also goes wrong direction sometimes



pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
from camera import Camera
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)


# load sprites
sprite_sheet_character = pygame.image.load('sprites/player.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_character)
sprite_sheet_upgrades = pygame.image.load("sprites/upgrades.png").convert_alpha()
background_image = pygame.image.load('sprites/ground.png').convert_alpha()
water = pygame.image.load('sprites/water.png').convert()
#scaled_background = pygame.transform.scale(background_image,3)

BLACK = (0, 0 ,0)

# Loading animations for each direction
animations = {'right': [], 'down': [], 'left': [], 'up': []}
for x in range(8):
    animations['right'].append(sprite_sheet.get_image(x, 100, 100, BLACK))
for x in range(8, 16):
    animations['down'].append(sprite_sheet.get_image(x, 100, 100, BLACK))
for x in range(16, 24):
    animations['left'].append(sprite_sheet.get_image(x, 100, 100, BLACK))
for x in range(24, 32):
    animations['up'].append(sprite_sheet.get_image(x, 100, 100, BLACK))
# Load attack images
attack_images = {
    'right': pygame.image.load('sprites/rightattack.PNG').convert_alpha(),
    'down': pygame.image.load('sprites/downattack.PNG').convert_alpha(),
    'left': pygame.image.load('sprites/leftattack.PNG').convert_alpha(),
    'up': pygame.image.load('sprites/upattack.PNG').convert_alpha()
}

# Load sword images
sword_images = {
    'right': pygame.image.load('sprites/rightsword.PNG').convert_alpha(),
    'down': pygame.image.load('sprites/downsword.PNG').convert_alpha(),
    'left': pygame.image.load('sprites/leftsword.PNG').convert_alpha(),
    'up': pygame.image.load('sprites/upsword.PNG').convert_alpha()
}
ghost = pygame.image.load('sprites/ghost.png').convert_alpha()

# Initialize a player

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 1, TILE_SIZE, TILE_SIZE)


walls = []
for i in range(len(MAP)):
    for j in range(len(MAP[i])):
        if MAP[i][j] == 'x' or MAP[i][j] == 'w':                                            
            walls.append(pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))


last_spawn_time = pygame.time.get_ticks()
last_spawn_time = pygame.time.get_ticks()

title_screen = TitleScreen(screen)
title_screen_active = True

while title_screen_active:
    title_screen.draw_background()
    title_screen.draw()
    
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            title_screen_active = False
            running = False
        if title_screen.handle_events(event):
            title_screen_active = False

last_fireball_time = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    keys = pygame.key.get_pressed()

    if player.need_to_choose_upgrade:
        screen.fill((255, 255, 255))
        for i in range(3):
            upgrade_to_draw = player.available_upgrades[i]
            source_rect = pygame.Rect(32*upgrade_to_draw.icon_ID,0,32,32)
            screen.blit(sprite_sheet_upgrades, (i*48,0), source_rect)
            screen.blit(sprite_sheet_upgrades, (i*48,48), pygame.Rect(32*i,32,32,32))
        pygame.display.update()

        if keys[pygame.K_1]:
            player.aquire_upgrade(player.available_upgrades[0].name)
        elif keys[pygame.K_2]:
            player.aquire_upgrade(player.available_upgrades[1].name)
        elif keys[pygame.K_3]:
            player.aquire_upgrade(player.available_upgrades[2].name)

        if keys[pygame.K_1] or keys[pygame.K_2] or keys[pygame.K_3]:
            player.need_to_choose_upgrade = False
        else:
            continue
    player.handle_collisions(Enemy.active_enemies, walls)

    for wall in walls:
        if MAP[wall.top // TILE_SIZE][wall.left // TILE_SIZE] == 'w':
            pygame.draw.rect(screen, (0, 0, 255), wall)

    player.update_projectiles()

    if keys[pygame.K_l]:
        player.add_experience(10)
        print(player.experience)


    current_time = pygame.time.get_ticks()
    if keys[pygame.K_2] and player.mana >= 20 and current_time - last_fireball_time > 2000:
        fireball = Fireball(player.x, player.y, player.direction)
        player.projectiles.append(fireball)
        player.mana -= 20
        last_fireball_time = current_time
    player.handle_movement(keys, walls)  
    player.regenerate_mana()
    # Check for sword collisions with enemies  
    player.check_sword_collisions(Enemy.active_enemies)  

    if player.is_attacking:
        if pygame.time.get_ticks() - player.attack_start_time > Player.attack_duration:
            player.is_attacking = False

    
    # Calculate camera offsetadjust_
    last_spawn_time = Enemy.spawn_enemies(last_spawn_time)
    camera.calculate_camera_offset(player)
    screen.fill((0))

    player.update_animation()

    camera.draw_with_offset(screen, water, (-2000, -1100))
    camera.draw_with_offset(screen, background_image, (0, 0))

    blue_square = pygame.Surface((TILE_SIZE, TILE_SIZE))
    blue_square.fill((0, 0, 255))
    for wall in walls:
        if MAP[wall.top // TILE_SIZE][wall.left // TILE_SIZE] == 'w':
            camera.draw_with_offset(screen, blue_square, (wall.left, wall.top))
    
    for projectile in player.projectiles:
      if isinstance(projectile, Fireball):
          projectile.update()
          projectile.render(screen, camera)
      if hasattr(projectile, 'remove') and projectile.remove:
            player.projectiles.remove(projectile)
            continue

      else:
          # Handle rendering for other types of projectiles here
          pass

    if player.is_attacking:
        camera.draw_with_offset(screen, attack_images[player.direction], (player.x, player.y))

        # Displaying the sword image during attack
        offset_x, offset_y = player.get_item_offset()
        camera.draw_with_offset(screen, sword_images[player.direction], (player.x + offset_x, player.y + offset_y)) 
 
        
    else:
        camera.draw_with_offset(screen, animations[player.direction][player.frame], (player.x, player.y))
    player.render_mana_bar(screen)

    
    # Draw fps counter 
    fps = clock.get_fps()
    fps_surface = font.render(f"FPS: {fps:.2f}", True, pygame.Color('white'))
    screen.blit(fps_surface, (10, 10)) 

    # Draw the enemy to the screen
    for enemy in Enemy.active_enemies:
        enemy.move_towards_player(player, walls)
        enemy.draw(screen, camera)
    
    # Draw the projectile as
    player.render_projectiles(screen, camera)
    Enemy.display_wave_number(screen, font)
    player.draw_health(screen, SCREEN_WIDTH)
    pygame.display.update()
    if player.health <= 0:
        break
   # for enemey in Enemy.active_enemies:
    #  print(enemy.health)
    clock.tick(60)
pygame.quit() 