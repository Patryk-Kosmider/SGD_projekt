import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type):
        super().__init__()
        self.type = enemy_type
        params = enemy_type.value
        img = pygame.image.load(params["image"]).convert_alpha()
        self.image = pygame.transform.scale(img, (50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = params["speed"]
        self.hp = params["hp"]
        self.damage = params["damage"]

    def update(self, enemy):
        dx, dy = (
            enemy.rect.centerx - self.rect.centerx,
            enemy.rect.centery - self.rect.centery,
        )
        dist = max(1, (dx**2 + dy**2) ** 0.5)
        self.rect.x += dx / dist * self.speed
        self.rect.y += dy / dist * self.speed
