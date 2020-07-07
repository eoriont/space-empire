from Unit.Unit import Unit


class ShipYard(Unit):
    # Shipyard unit stats
    cp_cost = 6
    attack_class = 'C'
    defense_strength = 0
    attack_strength = 3
    armor = 1
    abbr = 'SY'
    hull_size = 1
    req_size_tech = 1

    def __init__(self, *args):
        super().__init__(*args)
        self.maitenance_cost = 0
