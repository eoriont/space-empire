from Unit.Unit import Unit


class Base(Unit):
    attack_class = "A"
    attack_strength = 7
    defense_strength = 2
    armor = 3
    req_size_tech = 2

    def __init__(self, *args):
        super().__init__(*args)
        self.maitenance_cost = 0

    def get_possible_translations(self):
        return [self.pos]
