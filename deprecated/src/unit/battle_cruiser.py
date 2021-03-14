from unit import Unit


class BattleCruiser(Unit):
    # Battle cruiser unit's stats
    cp_cost = 15
    attack_class = 'B'
    attack_strength = 5
    defense_strength = 1
    abbr = "BC"
    armor = 2
    hull_size = 2
    req_size_tech = 4
