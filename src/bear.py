import pygame


class Bear(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        image = "../assets/bear_in.png"
        raw_image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(raw_image, (128, 128))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7
        self.hp = 3
        self.triple_shot = False
        self.invincible = False
        self.double_damage = False
        self.active_powerups = []

    def move(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        self.rect.clamp_ip(pygame.Rect(0, 0, 1280, 720))
