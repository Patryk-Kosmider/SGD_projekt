import configparser
import random
import pygame
import sys
from bear import Bear
from shooting import Shooting
from src.crosshair import Crosshair
from src.enemy import Enemy
from src.enemyType import EnemyType

config = configparser.ConfigParser()
config.read("config.ini")
width = config.getint("screen", "width")
height = config.getint("screen", "height")
fps = config.getint("screen", "fps")

MENU = "menu"
INSTRUCTIONS = "instructions"
RUNNING = "running"
EXIT = "exit"


def star_wars_intro(screen, text_lines, width, height):
    pygame.mixer.init()
    pygame.mixer.music.load("../assets/starwars_music.wav")
    pygame.mixer.music.play(-1)

    bear_img = pygame.image.load("../assets/bear.png").convert_alpha()
    bear_img = pygame.transform.scale(bear_img, (150, 150))

    clock = pygame.time.Clock()
    font = pygame.font.Font("../assets/PixelifySans-VariableFont_wght.ttf", 32)
    black = (0, 0, 0)
    yellow = (255, 255, 0)

    rendered_lines = [font.render(line, True, yellow) for line in text_lines]

    y_start = height

    running = True
    while running:
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                running = False

        for i, line_surface in enumerate(rendered_lines):
            y_pos = y_start + i * 50
            if y_pos > -50:
                screen.blit(line_surface, (width // 8, y_pos))

        img_y = y_start + len(rendered_lines) * 60
        if img_y > -300:
            img_rect = bear_img.get_rect(center=(width // 2, img_y))
            screen.blit(bear_img, img_rect)
        else:
            running = False

        y_start -= 1.2

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()


def draw_text(surface, text, size, x, y, color=(255, 255, 255)):
    font = pygame.font.Font("../assets/PixelifySans-VariableFont_wght.ttf", size)
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, rect)


def menu(screen, logo_img):
    pygame.mixer.init()
    pygame.mixer.music.load("../assets/csgo_music.wav")
    pygame.mixer.music.play(-1)
    screen.fill((200, 0, 0))
    options = ["Start", "Instrukcja", "Wczytaj zapis", "Wyjście"]
    selected = 0
    clock = pygame.time.Clock()

    while True:

        logo_rect = logo_img.get_rect(center=(width // 2, 150))
        screen.blit(logo_img, logo_rect)

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            draw_text(screen, option, 32, width // 2, 300 + i * 50, color)

        pygame.display.flip()
        clock.tick(15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return EXIT
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        return RUNNING
                    elif selected == 1:
                        instructions(screen)
                        screen.fill((200, 0, 0))
                        pygame.display.flip()
                    elif selected == 2:
                        return "load"
                    elif selected == 3:
                        return EXIT


def instructions(screen):
    screen.fill((200, 0, 0))
    draw_text(screen, "Instrukcja:", 32, width // 2, 100)
    draw_text(screen, "Sterowanie - WASD lub strzałki", 32, width // 2, 200)
    draw_text(screen, "Celowanie - za pomocą myszki", 32, width // 2, 250)
    draw_text(screen, "Strzelanie - lewy przycisk myszki", 32, width // 2, 300)
    draw_text(screen, "[P] - pauza", 32, width // 2, 350)
    draw_text(screen, "[ESC] - powrót do menu głównego]", 32, width // 2, 400)
    draw_text(
        screen, "Gra zapisuje się automatycznie przy wyjściu.", 32, width // 2, 450
    )

    pygame.display.flip()

    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return


def spawn_enemy(x, y, wave):
    weights = {
        EnemyType.ENEMY1: max(10 - wave, 1),
        EnemyType.ENEMY2: max(wave - 3, 1),
        EnemyType.ENEMY3: max(wave - 6, 1),
        EnemyType.ENEMY4: max(wave - 10, 1),
    }
    types = list(weights.keys())
    chances = [weights[t] for t in types]
    enemy_type = random.choices(types, weights=chances, k=1)[0]
    return Enemy(x, y, enemy_type)


def run_game(screen):
    clock = pygame.time.Clock()
    bear = Bear(width // 2, height // 2)
    all_sprites = pygame.sprite.Group(bear)
    shots = pygame.sprite.Group()
    crosshair = Crosshair()
    enemies = pygame.sprite.Group()

    pygame.mouse.set_visible(False)

    wave = 1
    spawn_timer = 0
    spawn_interval = 5000
    invulnerability_timer = 0

    run = True
    while run:
        frame = clock.tick(fps)
        spawn_timer += frame
        if invulnerability_timer > 0:
            invulnerability_timer -= frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                shooting = Shooting(bear.rect.centerx, bear.rect.centery, mx, my)
                shots.add(shooting)

        keys = pygame.key.get_pressed()
        bear.move(keys)

        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            mobs_per_wave = 5 + wave * 2
            for _ in range(mobs_per_wave):
                side = random.choice(["l", "r", "u", "d"])
                if side == "l":
                    x = -50
                    y = random.randint(0, height)
                elif side == "r":
                    x = width + 50
                    y = random.randint(0, height)
                elif side == "u":
                    x = random.randint(0, width)
                    y = -50
                elif side == "d":
                    x = random.randint(0, width)
                    y = height + 50

                enemy = spawn_enemy(x, y, wave)
                enemies.add(enemy)

            wave += 1

        enemies.update(bear)
        shots.update()

        for shot in shots:
            hit_enemies = pygame.sprite.spritecollide(shot, enemies, False)
            for enemy in hit_enemies:
                enemy.hp -= 1
                shot.kill()
                if enemy.hp <= 0:
                    enemy.kill()

        damage_enemies = pygame.sprite.spritecollide(bear, enemies, False)
        for enemy in damage_enemies:
            if invulnerability_timer <= 0:
                bear.hp -= enemy.damage
                invulnerability_timer = 1000
                if bear.hp <= 0:
                    run = False

        screen.fill((0, 0, 0))

        all_sprites.draw(screen)
        enemies.draw(screen)
        shots.draw(screen)
        crosshair.update()
        crosshair.draw(screen)

        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))

    intro_text = [
        "W odległej galaktyce...",
        "na planecie Ziemia...",
        "las młodego niedźwiedzia...",
        "został pożarty przez stwory z innego wymiaru...",
        "pozostawiony sam musi stawić im czoła...",
        "czy mały misiek da radę przetrwać...",
        "pomóż mu odzyskać jego las...",
    ]

    star_wars_intro(screen, intro_text, width, height)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Kalashmiskov")
    logo = pygame.image.load("../assets/logo.png").convert_alpha()
    logo = pygame.transform.scale(logo, (600, 150))

    state = MENU

    while state != EXIT:
        if state == MENU:
            menu_result = menu(screen, logo)
            if menu_result == RUNNING:
                state = RUNNING
            elif menu_result == EXIT:
                state = EXIT
        elif state == RUNNING:
            run_game(screen)
            state = MENU

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
