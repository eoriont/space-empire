from unit import Unit


class Scout(Unit):
    # Scout unit's stats
    cp_cost = 6
    attack_class = 'E'
    attack_strength = 3
    defense_strength = 0
    abbr = "S"
    armor = 1
    default_tech = {'movement': 1}
    hull_size = 1
    req_size_tech = 1
