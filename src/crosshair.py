import pygame


class Crosshair:
    def __init__(self):
        raw_image = pygame.image.load("../assets/crosshair.png").convert_alpha()
        self.image = pygame.transform.scale(raw_image, (32, 32))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
