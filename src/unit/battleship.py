from unit import Unit


class Battleship(Unit):
    # Battleship unit's stats
    cp_cost = 20
    attack_class = 'A'
    attack_strength = 5
    defense_strength = 2
    abbr = "BS"
    armor = 3
    hull_size = 3
    req_size_tech = 5
