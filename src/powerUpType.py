import enum


class PowerType(enum.Enum):

    TRIPLE_SHOT = {
        "image": "../assets/3xshoot.png",
        "duration": 10000,
        "instant": False,
        "base_chance": 0.05,
    }

    INVINCIBLE = {
        "image": "../assets/invincible.jpg",
        "duration": 5000,
        "instant": False,
        "base_chance": 0.01,
    }

    DOUBLE_DAMAGE = {
        "image": "../assets/2xdmg.png",
        "duration": 8000,
        "instant": False,
        "base_chance": 0.05,
    }

    HEAL = {"image": "../assets/heal.png", "instant": True, "base_chance": 0.07}
