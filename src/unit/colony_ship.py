from unit.unit import Unit
from unit.colony import Colony


class Colonyship(Unit):
    # Colonyship unit's stats
    cp_cost = 8
    attack_strength = 0
    defense_strength = 0
    abbr = "CS"
    armor = 1
    hull_size = 1
    req_size_tech = 1
    default_tech = {'mov': 1}
    no_maintenance = True
    no_attack = True

    # If moved onto a planet, the ship will be replaced with a colony
    def move(self, new_pos):
        if self.game.board.on_unoccupied_planet(self.pos):
            col = self.player.build_unit(Colony, self.pos)
            self.destroy()
            # Inefficient
            self.game.board.create()
        super().move(new_pos)
