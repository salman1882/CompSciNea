import pygame
from spritesheet import SpriteSheet
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, MAP
from player import Player

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# load sprites
sprite_sheet_character = pygame.image.load('sprites/player.png').convert_alpha()
sprite_sheet = SpriteSheet(sprite_sheet_character)

background_image = pygame.image.load('sprites/ground.png').convert()

# Initialize a player
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 1, TILE_SIZE, TILE_SIZE, sprite_sheet)

walls = []
for i in range(len(MAP)):
    for j in range(len(MAP[i])):
        if MAP[i][j] == 'x':
            walls.append(pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1, 0, walls)
    if keys[pygame.K_RIGHT]:
        player.move(1, 0, walls)
    if keys[pygame.K_UP]:
        player.move(0, -1, walls)
    if keys[pygame.K_DOWN]:
        player.move(0, 1, walls)

    # Draw grid
    screen.fill((0))
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

    # Check for collisions and draw map
    for wall in walls:
        pygame.draw.rect(screen, (255, 0, 0), wall)
    
    # Draw player
    player.draw(screen)
    pygame.display.update()

pygame.quit()