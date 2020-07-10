from unit.unit import Unit
from unit.ship_yard import ShipYard
from unit.base import Base


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

    # If destroyed, destroy any remaining shipyards and bases
    def destroy(self):
        super().destroy()
        for unit in self.game.grid[self.pos]:
            if unit.player == self.player:
                if type(unit) in (ShipYard, Base):
                    unit.destroy()
