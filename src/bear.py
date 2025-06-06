import pygame
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


class Bear(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        image = "../assets/bear_in.png"
        raw_image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(raw_image, (128, 128))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = config.getint("bear", "speed")
        self.hp = 10

    def move(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            print("Gora")
            self.rect.y -= self.speed
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            print("Dol")
            self.rect.y += self.speed
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            print("Lewo")
            self.rect.x -= self.speed
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            print("Prawo")
            self.rect.x += self.speed

        self.rect.clamp_ip(pygame.Rect(0, 0, 1280, 720))
