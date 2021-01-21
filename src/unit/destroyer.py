from unit import Unit


class Destroyer(Unit):
    # Destroyer unit's stats
    cp_cost = 9
    attack_class = 'D'
    attack_strength = 4
    defense_strength = 0
    abbr = "DE"
    armor = 1
    hull_size = 1
    req_size_tech = 2
