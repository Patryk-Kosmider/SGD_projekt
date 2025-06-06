import math

import pygame


class Shooting(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 6))
        self.image.fill((255, 50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist == 0:
            dist = 1
        self.velocity = (dx / dist * 10, dy / dist * 10)

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not pygame.Rect(0, 0, 1280, 720).colliderect(self.rect):
            self.kill()
