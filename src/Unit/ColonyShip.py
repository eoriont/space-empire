from Unit.Unit import Unit
from Unit.Colony import Colony


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
    no_maitenance = True
    no_attack = True

    # If moved onto a planet, the ship will be replaced with a colony
    def move(self, new_pos):
        if self.game.grid.on_unoccupied_planet(self.pos):
            self.player.build_unit(Colony, self.pos)
            self.destroy()
        super().move(new_pos)
