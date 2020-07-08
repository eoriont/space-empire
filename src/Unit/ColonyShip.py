from Unit.Unit import Unit
from Unit.Colony import Colony


class Colonyship(Unit):
    # Colonyship unit's stats
    cp_cost = 8
    attack_class = 'Z'
    attack_strength = 0
    defense_strength = 0
    abbr = "CS"
    armor = 1
    hull_size = 1
    req_size_tech = 1
    default_tech = {'spd': 0}
    no_maitenance = True

    # If moved onto a planet, the ship will be replaced with a colony
    def move(self, new_pos):
        planet_positions = [planet.pos for planet in self.game.planets]
        if self.pos in planet_positions:
            units = self.game.unit_grid[self.pos]
            if Colony not in [type(unit) for unit in units]:
                self.player.build_unit(Colony)
                self.destroy()
        super().move(new_pos)
