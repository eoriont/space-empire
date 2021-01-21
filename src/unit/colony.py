from unit import Unit, ShipYard, Base


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

    def __init__(self, *args, home_colony=False):
        super().__init__(*args)
        self.is_home_colony = home_colony

    # Remove 1 cp_capacity if hurt

    def hurt(self):
        self.cp_capacity -= 1
        if self.cp_capacity <= 0:
            self.destroy()

    # If destroyed, destroy any remaining shipyards and bases
    def destroy(self, reason):
        super().destroy(reason)
        for unit in self.game.board[self.pos]:
            if unit.player == self.player:
                if type(unit) in (ShipYard, Base):
                    unit.destroy(reason)
