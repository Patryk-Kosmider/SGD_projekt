import math

import pygame


class Shooting(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, angle_offset=0):
        super().__init__()
        self.og_image = pygame.Surface((10, 6), pygame.SRCALPHA)
        self.og_image.fill((255, 50, 50))

        dx = target_x - x
        dy = target_y - y
        base_angle = math.atan2(dy, dx)

        angle_with_offset = base_angle + angle_offset

        vel_x = math.cos(angle_with_offset) * 10
        vel_y = math.sin(angle_with_offset) * 10
        self.velocity = (vel_x, vel_y)

        # Obrót sprite'a
        rot_angle = -math.degrees(angle_with_offset)
        self.image = pygame.transform.rotate(self.og_image, rot_angle)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not pygame.Rect(0, 0, 1280, 720).colliderect(self.rect):
            self.kill()
