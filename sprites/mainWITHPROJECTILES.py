# Create an instance of the Enemy class using the "ghost" image
from enemy import Enemy
import pygame
import spritesheet
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, MAP
from player import *
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

attack_start_time = 0
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
        if MAP[i][j] == 'x':                                            
            walls.append(pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))



last_spawn_time = pygame.time.get_ticks()
last_spawn_time = pygame.time.get_ticks()

title_screen = TitleScreen(screen)
title_screen_active = True

while title_screen_active:
    title_screen.draw()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            title_screen_active = False
            running = False
        if title_screen.handle_events(event):
            title_screen_active = False
running = True
while running:
    player.handle_collisions(Enemy.active_enemies, walls)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_2]:
        player.switch_weapon()

    player.handle_movement(keys, walls)

    player.handle_projectiles(Enemy.active_enemies, walls)
    
    player.check_weapon_collisions(Enemy.active_enemies)  # Check for weapon collisions with enemies


    if player.is_attacking:
        if pygame.time.get_ticks() - player.attack_start_time > Player.attack_cooldown:
            player.is_attacking = False

    
    # Calculate camera offset
    last_spawn_time = Enemy.spawn_enemies(last_spawn_time)
    camera.calculate_camera_offset(player)
    screen.fill((0))

    player.update_animation()


    # draws red walls where "X" is on tilemap
    for wall in walls:
        pygame.draw.rect(screen, (255, 0, 0), camera.apply_offset(wall))
    
    camera.draw_with_offset(screen, water, (-2000, -1100))
    camera.draw_with_offset(screen, background_image, (0, 0))

    if player.is_attacking:
        camera.draw_with_offset(screen, attack_images[player.direction], (player.x, player.y))

        # Displaying the sword image during attack
        offset_x, offset_y = player.get_sword_offset()
        camera.draw_with_offset(screen, sword_images[player.direction], (player.x + offset_x, player.y + offset_y))
 
        
    else:
        camera.draw_with_offset(screen, animations[player.direction][player.frame], (player.x, player.y))

    
    
    fps = clock.get_fps()
    fps_surface = font.render(f"FPS: {fps:.2f}", True, pygame.Color('white'))
    screen.blit(fps_surface, (10, 10))

    # Draw the enemy to the screen
    for enemy in Enemy.active_enemies: 
        enemy.move_towards_player(player)
        enemy.draw(screen, camera)
    
    
    # Draw projectiles
    for projectile in player.projectiles:
        projectile_rect = pygame.Rect(*projectile['position'], 10, 10) # Example projectile size
        pygame.draw.rect(screen, (255, 255, 255), camera.apply_offset(projectile_rect))

    player.draw_health(screen, SCREEN_WIDTH)

    pygame.display.update()
    clock.tick(60)
pygame.quit()