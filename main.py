import pygame
import spritesheet
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, MAP
from player import Player

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

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

# Initialize a player
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 1, TILE_SIZE, TILE_SIZE)

walls = []
for i in range(len(MAP)):
    for j in range(len(MAP[i])):
        if MAP[i][j] == 'x':
            walls.append(pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))

animation_cooldown = 80
frame = 0
last_update = pygame.time.get_ticks()


def calculate_camera_offset(target, screen_width, screen_height):
    x = -target.x + screen_width // 2
    y = -target.y + screen_height // 2
    return x, y
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-10, 0, walls)
    if keys[pygame.K_RIGHT]:
        player.move(10, 0, walls)
    if keys[pygame.K_UP]:
        player.move(0, -10, walls)
    if keys[pygame.K_DOWN]:
        player.move(0, 10, walls)

    # Draw grid
    
    # Calculate camera offset
    camera_offset_x, camera_offset_y = calculate_camera_offset(player, SCREEN_WIDTH, SCREEN_HEIGHT)
    screen.fill((0))

    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame = frame + 1 
        last_update = current_time
        if frame >= 8:
            frame = 0

    for wall in walls:
        pygame.draw.rect(screen, (255, 0, 0), wall.move(camera_offset_x, camera_offset_y))
    
    screen.blit(water, (camera_offset_x - 2000, camera_offset_y - 1100))
    screen.blit(background_image, (camera_offset_x, camera_offset_y))
    screen.blit(animations[player.direction][frame], (player.x + camera_offset_x, player.y + camera_offset_y))
    
    fps = clock.get_fps()
    fps_surface = font.render(f"FPS: {fps:.2f}", True, pygame.Color('white'))
    screen.blit(fps_surface, (10, 10))
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
