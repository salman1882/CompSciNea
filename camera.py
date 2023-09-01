import pygame

class Camera:
    def __init__(self, screen_width, screen_height):
        # Initialize the camera
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset_x = 0
        self.offset_y = 0
        self.lerp_factor = 0.2
    def lerp(self, start, end):
        return (1 - self.lerp_factor) * start + self.lerp_factor * end
    def calculate_camera_offset(self, target):
         # Calculate the desired camera's offset based on the given target's position
        # This would center the target in the middle of the screen
        desired_offset_x = -target.x + self.screen_width // 2
        desired_offset_y = -target.y + self.screen_height // 2

        # Smoothly transition the current offset to the desired offset using lerp
        self.offset_x = self.lerp(self.offset_x, desired_offset_x)
        self.offset_y = self.lerp(self.offset_y, desired_offset_y)

    def apply_offset(self, rect):
        # Adjust a rectangle's position based on the camera's offset
        return rect.move(self.offset_x, self.offset_y)

    def draw_with_offset(self, screen, image, position):
        # Draw an image on the screen with the camera's offset applied
        adjusted_position = (position[0] + self.offset_x, position[1] + self.offset_y)
        screen.blit(image, adjusted_position)