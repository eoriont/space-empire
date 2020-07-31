from player.player import Player
import random
from unit.scout import Scout
from technology import Technology
from unit.scout import Scout
from unit.colony_ship import Colonyship
from unit.ship_yard import ShipYard
from unit.colony import Colony
from unit.destroyer import Destroyer
from unit.cruiser import Cruiser
from unit.battle_cruiser import BattleCruiser
from unit.dreadnaught import Dreadnaught
from unit.battleship import Battleship
from unit.decoy import Decoy
from unit.base import Base


class RandomPlayer(Player):
    # Builds a fleet of random units within the player's budget
    def build_fleet(self):
        unit_list = [Scout, Destroyer, Cruiser,
                     BattleCruiser, Battleship, Dreadnaught, Colonyship, Decoy, ShipYard, Base]
        unit_list = [
            unit for unit in unit_list if unit.req_size_tech <= self.tech['ss']]

        planet_positions = [planet.pos for planet in self.game.board.planets]
        shipyard_available = [shipyard for shipyard in self.units
                              if type(shipyard) == ShipYard
                              and shipyard.pos in planet_positions]
        if len(shipyard_available) == 0:
            # There are no shipyards on planets, so units can't be build
            return
        positions = {}
        for shipyard in shipyard_available:
            if shipyard.pos not in positions:
                positions[shipyard.pos] = 0
            positions[shipyard.pos] += shipyard.tech['syc']
        # The cheapest unit is a decoy at 1 cp
        while self.construction_points >= 6:
            pos = random.choice(list(positions))
            capacity = positions[pos]
            capacity += 1
            capacity /= 2
            available_units = [unit for unit in unit_list if unit.cp_cost <=
                               self.construction_points and unit.hull_size <= capacity]
            self.build_unit(random.choice(available_units), pos)

    # Upgrade a certain technology
    def upgrade_tech(self):
        options = self.tech.get_available(self.construction_points)
        if len(options) == 0:
            return
        choice = random.choice(options)
        self.construction_points -= self.tech.buy_tech(choice)

    # Move units to random spots
    def move_units(self, phase):
        for unit in self.units:
            unit.move(random.choice(
                unit.get_possible_spots(phase)))
