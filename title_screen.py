
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class TitleScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.play_button = pygame.Rect(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 20, 140, 40)
        self.play_button_image = pygame.image.load('sprites/main_menu/play_button.png')
        self.play_button_image = pygame.transform.scale(self.play_button_image, (140, 40))
        self.layers = [] 
        for i in range(1, 6):  # 5 layers
            layer = pygame.image.load(f'sprites/main_menu/{i}.png')
            layer = pygame.transform.scale(layer, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.layers.append(layer)
        self.layer_positions = [(0, 0) for _ in range(5)]
        

    def draw(self):
        self.screen.blit(self.play_button_image, (self.play_button.x, self.play_button.y))
    def draw_background(self):
        speeds = [0.5, 0.75, 1, 1.25, 1.5] # different speeds for each image for parralax effect
        for i in range(len(self.layers)):
         layer = self.layers[i]
         x, y = self.layer_positions[i]
         self.screen.blit(layer, (x, y)) # draw layer
         if x <= 0: # if part of layer is off screen
          self.screen.blit(layer, (x + layer.get_width(), y)) # draw duplicate layer to fill in blank
         new_x = x - speeds[i]
         if new_x <= -layer.get_width(): # if layer is completly off screen
             new_x = 0
         self.layer_positions[i] = (new_x, y) # update positon of layer to nex_x 


    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.play_button.collidepoint(mouse_pos):
                return True
        return False
