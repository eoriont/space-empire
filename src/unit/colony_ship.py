from unit import Unit

class ColonyShip(Unit):
    # ColonyShip unit's stats
    cp_cost = 8
    attack_strength = 0
    defense_strength = 0
    abbr = "CS"
    armor = 1
    hull_size = 1
    req_size_tech = 1
    default_tech = {'movement': 1}
    no_maintenance = True
    no_attack = True
    name = "ColonyShip"
