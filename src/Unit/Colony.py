from Unit.Unit import Unit


class Colony(Unit):
    # Colony unit's stats
    cp_cost = 0
    cp_capacity = 3
    attack_strength = 0
    defense_strength = 0
    abbr = "CO"
    no_maitenance = True
    no_attack = True
    immovable = True

    # Remove 1 cp_capacity if hurt
    def hurt(self):
        self.cp_capacity -= 1
        if self.cp_capacity <= 0:
            self.destroy()
