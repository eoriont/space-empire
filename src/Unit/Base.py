from Unit.Unit import Unit


class Base(Unit):
    attack_class = "A"
    attack_strength = 7
    defense_strength = 2
    armor = 3
    req_size_tech = 2
    no_maitenance = True

    def get_possible_translations(self):
        return [self.pos]
