from Unit.Unit import Unit


class Colony(Unit):
    # Colony unit's stats
    cp_cost = 0
    cp_capacity = 3
    attack_class = "Z"
    attack_strength = 0
    defense_strength = 0
    abbr = "CO"
    no_maitenance = True

    # Remove 1 cp_capacity if hurt
    def hurt(self):
        self.cp_capacity -= 1
        super().hurt()

    def get_possible_spots(self):
        return [self.pos]
