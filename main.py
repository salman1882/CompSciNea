import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, MAP
from player import Player

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Initialize a player
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 1, TILE_SIZE, TILE_SIZE)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1, 0)
    if keys[pygame.K_RIGHT]:
        player.move(1, 0)
    if keys[pygame.K_UP]:
        player.move(0, -1)
    if keys[pygame.K_DOWN]:
        player.move(0, 1)

    # Draw grid
    screen.fill((0))
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

    # Check for collisions and draw map
    for i, row in enumerate(MAP):
        for j, tile in enumerate(row):
            if tile == 'x':  # wall
                wall_rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, (255, 0, 0), wall_rect)  # Draw red wall
                if player.collides_with(wall_rect):
                    print("Collision!")

    # Draw player
    player.draw(screen)
    pygame.display.update()

pygame.quit()