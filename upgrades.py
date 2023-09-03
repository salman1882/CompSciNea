class Upgrade:
    def __init__(self, name, is_repeatable, description, icon_ID, effect, rarity):
        self.name = name
        self.description = description
        self.icon_ID = icon_ID
        self.is_repeatable = is_repeatable
        self.effect = effect
        self.rarity = rarity

def health_boost(player):
	player.max_health += 1

def mana_boost(player):
	player.max_mana += 10
def speed_boost(player):
	player.speed *= 1.1
def mana_regen_boost(player):
	player.mana_regen_rate *= 1.25
def load_upgrades(player):
	return {
		"health_boost": Upgrade("health_boost", True, "Increases the amount of hearts you have by one", 0 , health_boost, 50),
		"mana_boost": Upgrade("mana_boost", True, "Increases the amount of maximum mana you have by 10", 1 , mana_boost, 100),
		"speed_boost": Upgrade("speed_boost", True, "Increases your movement speed by 10% (multiplicatively)", 3 , speed_boost, 100),
		"mana_regen_boost": Upgrade("mana_regen_boost", True, "Increases your mana regeneration rate by 25% (multiplicatively)", 2 , mana_regen_boost, 100)
	}