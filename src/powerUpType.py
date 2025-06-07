import enum


class PowerType(enum.Enum):

    TRIPLE_SHOT = {
        "image": "../assets/enemy_1.jpg",
        "duration": 10000,
        "instant": False,
        "base_chance": 0.05,
    }

    INVINCIBLE = {
        "image": "../assets/enemy_2.jpg",
        "duration": 5000,
        "instant": False,
        "base_chance": 0.01,
    }

    DOUBLE_DAMAGE = {
        "image": "../assets/enemy_3.png",
        "duration": 8000,
        "instant": False,
        "base_chance": 0.05,
    }

    HEAL = {"image": "../assets/enemy_4.jpg", "instant": True, "base_chance": 0.07}
