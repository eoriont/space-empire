from unit import Unit

class Colony(Unit):
    # Colony unit's stats
    cp_cost = 0
    cp_capacity = 3
    attack_strength = 0
    defense_strength = 0
    abbr = "CO"
    no_maintenance = True
    no_attack = True
    immovable = True
    name = "Colony"
