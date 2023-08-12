import pygame

class Camera:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset_x = 0
        self.offset_y = 0

    def calculate_camera_offset(self, target):
        self.offset_x = -target.x + self.screen_width // 2
        self.offset_y = -target.y + self.screen_height // 2

    def apply_offset(self, rect):
        return rect.move(self.offset_x, self.offset_y)

    def draw_with_offset(self, screen, image, position):
        adjusted_position = (position[0] + self.offset_x, position[1] + self.offset_y)
        screen.blit(image, adjusted_position)
