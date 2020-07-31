from player.player import Player
from unit.scout import Scout
from unit.destroyer import Destroyer


class CombatPlayer(Player):
    current_ship_to_buy = "Destroyer"

    # Upgrade ship size tech to 2
    def upgrade_tech(self):
        while True:
            if self.tech['ss'] < 2 and 'ss' in self.tech.get_available(self.construction_points):
                self.construction_points -= self.tech.buy_tech('ss')
            else:
                break

    # Buy a scout or destroyer
    def build_fleet(self):
        ships = {"Scout": Scout, "Destroyer": Destroyer}
        ship_to_buy = ships[self.current_ship_to_buy]
        if ship_to_buy.req_size_tech < self.tech['ss']:
            ship_to_buy = Scout
        if self.construction_points >= ship_to_buy.cp_cost:
            self.build_unit(ship_to_buy)

    # Move all units
    def move_units(self, phase):
        for unit in self.units:
            self.move_towards_center(unit, phase)

    # Move to the square closest to the center
    def move_towards_center(self, unit, phase):
        if unit.pos == self.game.board.center:
            return
        possible_spaces = unit.get_possible_spots(phase)
        distances = [dist(self.game.board.center, pos)
                     for pos in possible_spaces]
        next_space = possible_spaces[distances.index(min(distances))]
        unit.move(next_space)

    # Choose the first unit to attack
    def choose_unit_to_attack(self, units):
        return units[0]

    # Don't screen any units
    def screen_units(self):
        return []


def dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x1 - x2)**2 + (y1 - y2)**2)**.5
