import pygame


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, powertype):
        super().__init__()
        self.type = powertype
        params = powertype.value
        self.image = pygame.image.load(params["image"]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(center=(x, y))
