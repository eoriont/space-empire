from unit import Unit

class Shipyard(Unit):
    # Shipyard unit stats
    cp_cost = 6
    attack_class = 'C'
    defense_strength = 0
    attack_strength = 3
    armor = 1
    abbr = 'SY'
    hull_size = 1
    req_size_tech = 1
    no_maintenance = True
    immovable = True
    name = "Shipyard"
