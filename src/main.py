import configparser
import random
import pygame
import sys
from bear import Bear
from shooting import Shooting
from src.crosshair import Crosshair
from src.enemy import Enemy
from src.enemyType import EnemyType
from src.powerUp import PowerUp
from src.powerUpType import PowerType

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
    pygame.mixer.music.set_volume(0.1)
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


def draw_text(surface, text, size, x, y, color=(255, 255, 255), align="center"):
    font = pygame.font.Font("../assets/PixelifySans-VariableFont_wght.ttf", size)
    text_surface = font.render(text, True, color)
    if align == "center":
        rect = text_surface.get_rect(center=(x, y))
    elif align == "topleft":
        rect = text_surface.get_rect(topleft=(x, y))
    elif align == "topright":
        rect = text_surface.get_rect(topright=(x, y))
    surface.blit(text_surface, rect)


def menu(screen, logo_img):
    pygame.mixer.init()
    pygame.mixer.music.load("../assets/csgo_music.wav")
    pygame.mixer.music.play(-1)

    volume = 0.5
    muted = False
    volume_icon = pygame.image.load("../assets/sound.png").convert_alpha()
    volume_icon_muted = pygame.image.load("../assets/mute_sound.png").convert_alpha()
    volume_icon = pygame.transform.scale(volume_icon, (40, 40))
    volume_icon_muted = pygame.transform.scale(volume_icon_muted, (40, 40))

    screen.fill((200, 0, 0))
    options = ["Start", "Instrukcja", "Historia wyników", "Wyjście"]
    selected = 0
    clock = pygame.time.Clock()

    while True:

        logo_rect = logo_img.get_rect(center=(width // 2, 150))
        screen.blit(logo_img, logo_rect)

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            draw_text(screen, option, 32, width // 2, 300 + i * 50, color)

        icon_pos = (width - 50, height - 50)
        if muted:
            screen.blit(volume_icon_muted, icon_pos)
        else:
            screen.blit(volume_icon, icon_pos)

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
                        return show_score_history(screen)
                    elif selected == 3:
                        return EXIT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                ix, iy = icon_pos
                if ix <= mx <= ix + 40 and iy <= my <= iy + 40:
                    muted = not muted
                    pygame.mixer.music.set_volume(0 if muted else volume)


def instructions(screen):
    screen.fill((200, 0, 0))
    draw_text(screen, "Instrukcja:", 32, width // 2, 100)
    draw_text(screen, "Sterowanie - WASD lub strzałki", 32, width // 2, 200)
    draw_text(screen, "Celowanie - za pomocą myszki", 32, width // 2, 250)
    draw_text(screen, "Strzelanie - lewy przycisk myszki", 32, width // 2, 300)
    draw_text(screen, "[P] - pauza", 32, width // 2, 350)
    draw_text(screen, "[ESC] - powrót do menu głównego]", 32, width // 2, 400)
    draw_text(screen, "[R] - zrestartuj grę", 32, width // 2, 450)

    pygame.display.flip()

    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return


def show_score_history(screen):
    screen.fill((200, 0, 0))
    draw_text(screen, "Historia wyników", 40, width // 2, 50)
    scores = []
    with open("scores.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line.isdigit():
                scores.append(int(line))

    if scores:
        top_score = max(scores)
        draw_text(screen, f"Top score: {top_score}", 32, width // 2, 120, (255, 255, 0))
        draw_text(screen, "Ostatnie 10 wyników:", 28, width // 2, 170)

        last_scores = scores[-10:]
        last_scores.reverse()
        for i, score in enumerate(last_scores):
            draw_text(screen, f"{i + 1}. {score}", 24, width // 2, 210 + i * 30)
    else:
        draw_text(screen, "Brak zapisanych wyników.", 28, width // 2, 150)

    draw_text(screen, "Naciśnij [ESC], aby wrócić do menu", 24, width // 2, height - 50)

    pygame.display.flip()

    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                wait = False


def pause_menu(screen):
    background = screen.copy()
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    screen.blit(background, (0, 0))
    screen.blit(overlay, (0, 0))
    draw_text(screen, "PAUZA", 64, width // 2, height // 2 - 50)
    draw_text(
        screen, "Wciśnij [P], aby wrócić do gry", 32, width // 2, height // 2 + 20
    )
    pygame.display.flip()

    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                return


def game_over(screen, score):
    screen.fill((200, 0, 0))
    draw_text(screen, "Koniec gry!", 64, width // 2, height // 2 - 50, (255, 255, 255))
    draw_text(
        screen,
        f"Twój wynik: {score}",
        32,
        width // 2,
        height // 2 + 10,
        (255, 255, 255),
    )
    draw_text(
        screen,
        "Naciśnij [R], by zrestartować grę",
        32,
        width // 2,
        height // 2 + 50,
        (255, 255, 255),
    )
    draw_text(
        screen,
        "Naciśnij [ESC], żeby powrócić do menu",
        24,
        width // 2,
        height // 2 + 80,
        (255, 255, 255),
    )

    with open("scores.txt", "a") as f:
        f.write(f"{score}\n")

    pygame.display.flip()

    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return "restart"


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


def spawn_powerup(x, y, enemy, wave, powerups):
    kill_bonus = {
        1: 1.0,
        2: 1.2,
        3: 1.5,
        4: 2.0,
    }

    enemy_lvl = int(enemy.type.name[-1])
    multiplier = kill_bonus.get(enemy_lvl)

    wave_bonus = 1 + (wave * 0.03)

    for powertype in PowerType:
        chances = powertype.value["base_chance"] * multiplier * wave_bonus
        if random.random() < chances:
            powerup = PowerUp(x, y, powertype)
            powerups.add(powerup)


def powerup_effect(bear, powertype):
    if powertype == PowerType.TRIPLE_SHOT:
        bear.triple_shot = True
        pygame.time.set_timer(pygame.USEREVENT + 1, powertype.value["duration"])
        if powertype not in bear.active_powerups:
            bear.active_powerups.append(powertype)
    elif powertype == PowerType.INVINCIBLE:
        bear.invincible = True
        pygame.time.set_timer(pygame.USEREVENT + 2, powertype.value["duration"])
        if powertype not in bear.active_powerups:
            bear.active_powerups.append(powertype)
    elif powertype == PowerType.DOUBLE_DAMAGE:
        bear.double_damage = True
        pygame.time.set_timer(pygame.USEREVENT + 3, powertype.value["duration"])
        if powertype not in bear.active_powerups:
            bear.active_powerups.append(powertype)
    elif powertype == PowerType.HEAL:
        bear.hp += 1
        if bear.hp > 3:
            bear.hp = 3


def run_game(screen):
    background_img = pygame.image.load("../assets/map.png")
    background_img = pygame.transform.scale(background_img, (width, height))
    clock = pygame.time.Clock()
    bear = Bear(width // 2, height // 2)
    all_sprites = pygame.sprite.Group(bear)
    shots = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    crosshair = Crosshair()
    pygame.mouse.set_visible(False)

    wave = 0
    spawn_timer = 0
    spawn_interval = 5000
    invulnerability_timer = 0
    score = 0

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
                elif event.key == pygame.K_p:
                    pause_menu(screen)
                elif event.key == pygame.K_r:
                    return run_game(screen)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                if bear.triple_shot:
                    offsets = [-0.2, 0.0, 0.2]
                    for offset in offsets:
                        shooting = Shooting(
                            bear.rect.centerx,
                            bear.rect.centery,
                            mx,
                            my,
                            angle_offset=offset,
                        )
                        shots.add(shooting)
                else:
                    shooting = Shooting(bear.rect.centerx, bear.rect.centery, mx, my)
                    shots.add(shooting)

            elif event.type == pygame.USEREVENT + 1:
                bear.triple_shot = False
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)
                if PowerType.TRIPLE_SHOT in bear.active_powerups:
                    bear.active_powerups.remove(PowerType.TRIPLE_SHOT)
            elif event.type == pygame.USEREVENT + 2:
                bear.invincible = False
                pygame.time.set_timer(pygame.USEREVENT + 2, 0)
                if PowerType.INVINCIBLE in bear.active_powerups:
                    bear.active_powerups.remove(PowerType.INVINCIBLE)
            elif event.type == pygame.USEREVENT + 3:
                bear.double_damage = False
                pygame.time.set_timer(pygame.USEREVENT + 3, 0)
                if PowerType.DOUBLE_DAMAGE in bear.active_powerups:
                    bear.active_powerups.remove(PowerType.DOUBLE_DAMAGE)

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
        powerups.update()

        collected = pygame.sprite.spritecollide(bear, powerups, True)
        for powerup in collected:
            powerup_effect(bear, powerup.type)

        for shot in shots:
            hit_enemies = pygame.sprite.spritecollide(shot, enemies, False)
            for enemy in hit_enemies:
                damage = 2 if bear.double_damage else 1
                enemy.hp -= damage
                shot.kill()
                if enemy.hp <= 0:
                    score += enemy.points
                    enemy.kill()
                    spawn_powerup(
                        enemy.rect.centerx, enemy.rect.centery, enemy, wave, powerups
                    )

        damage_enemies = pygame.sprite.spritecollide(bear, enemies, False)
        for enemy in damage_enemies:
            if invulnerability_timer <= 0 and not bear.invincible:
                bear.hp -= enemy.damage
                invulnerability_timer = 1000
                if bear.hp <= 0:
                    result = game_over(screen, score)
                    if result == "restart":
                        run_game(screen)
                    else:
                        return

        screen.blit(background_img, (0,0))
        draw_text(
            screen, f"Punkty życia : {bear.hp}", 20, 10, 10, (255, 255, 255), "topleft"
        )
        draw_text(
            screen,
            f"Highscore: {score}",
            20,
            width - 10,
            10,
            (255, 255, 255),
            "topright",
        )
        draw_text(
            screen, f"Fala: {wave}", 20, width // 2, 10, (255, 255, 255), "center"
        )

        icon_x = 10
        icon_y = 40
        for powertype in bear.active_powerups:
            img = pygame.image.load(powertype.value["image"]).convert_alpha()
            img = pygame.transform.scale(img, (32, 32))
            screen.blit(img, (icon_x, icon_y))
            icon_x += 40

        all_sprites.draw(screen)
        enemies.draw(screen)
        shots.draw(screen)
        crosshair.update()
        crosshair.draw(screen)
        powerups.draw(screen)

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
