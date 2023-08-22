
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class TitleScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.play_button = pygame.Rect(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 20, 140, 40)

    def draw(self):
        pygame.draw.rect(self.screen, self.button_color, self.play_button)
        play_text = self.font.render('Play', True, self.text_color)
        self.screen.blit(play_text, (self.play_button.x + 45, self.play_button.y + 5))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.play_button.collidepoint(mouse_pos):
                return True
        return False
