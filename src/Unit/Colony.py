from Unit.Unit import Unit


class Colony(Unit):
    # Colony unit's stats
    cp_cost = 0
    buyable = False
    cp_capacity = 3
    attack_class = "Z"
    attack_strength = 0
    defense_strength = 0
    abbr = "CO"

    def __init__(self, *args):
        super().__init__(*args)
        self.maitenance_cost = 0

    # Remove 1 cp_capacity if hurt
    def hurt(self):
        self.cp_capacity -= 1
        if self.cp_capacity == 0:
            self.destroy()

    def get_possible_spots(self):
        return [self.pos]
