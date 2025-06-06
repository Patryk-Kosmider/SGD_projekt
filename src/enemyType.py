import enum


class EnemyType(enum.Enum):

    ENEMY1 = {
        "image": "../assets/enemy_1.jpg",
        "speed": 1.5,
        "hp": 1,
        "damage": 1,
    }

    ENEMY2 = {
        "image": "../assets/enemy_2.jpg",
        "speed": 1.2,
        "hp": 2,
        "damage": 1,
    }

    ENEMY3 = {
        "image": "../assets/enemy_3.png",
        "speed": 1,
        "hp": 3,
        "damage": 2,
    }

    ENEMY4 = {
        "image": "../assets/enemy_4.jpg",
        "speed": 0.5,
        "hp": 5,
        "damage": 3,
    }
