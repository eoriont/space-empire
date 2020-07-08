import random
from Technology import Technology
from Unit.Scout import Scout
from Unit.ColonyShip import Colonyship
from Unit.ShipYard import ShipYard
from Unit.Colony import Colony
from Unit.Destroyer import Destroyer
from Unit.Cruiser import Cruiser
from Unit.BattleCruiser import BattleCruiser
from Unit.Dreadnaught import Dreadnaught
from Unit.Battleship import Battleship


class Player:
    # Initialize player and build fleet
    def __init__(self, name, starting_pos, game=None, color="black"):
        self.starting_pos = starting_pos
        self.name = name
        self.units = []
        self.color = color
        self.game = game
        self.tech = Technology()
        self.construction_points = 20
        self.build_starting_fleet()
        self.construction_points = 20

    def get_player_by_name(self, name):
        for player in self.game.players:
            if player.name == name:
                return player

    # Build all the ships the player starts with
    def build_starting_fleet(self):
        for _ in range(3):
            self.build_unit(Scout)

        for _ in range(3):
            self.build_unit(Colonyship)

        for _ in range(4):
            self.build_unit(ShipYard)

        self.build_unit(Colony)

    # Give the player a specified amount of cp
    def pay(self, construction_points):
        self.construction_points += construction_points

    # Pay the maitenance cost of each unit
    def pay_maitenance_costs(self):
        for unit in self.units:
            cost = unit.maitenance_cost
            if self.construction_points >= cost:
                self.construction_points -= cost
            else:
                unit.destroy()

    # Upgrade a certain technology
    def upgrade_tech(self):
        options = self.tech.get_available(self.construction_points)
        if len(options) == 0:
            return
        choice = random.choice(options)
        self.construction_points -= self.tech.buy_tech(choice)

    # Remove unit from player's unit list
    def destroy_unit(self, unit):
        if unit in self.units:
            self.units.remove(unit)

    # Add unit to player's unit list
    def build_unit(self, unit_type, starting_pos=None):
        starting_pos = self.starting_pos if starting_pos is None else starting_pos
        unit = unit_type(
            self, f"{unit_type.abbr}{len(self.units)+1}", starting_pos, self.game, self.tech)
        self.construction_points -= unit.cp_cost
        self.units.append(unit)

    # Builds a fleet of random units within the player's budget
    def build_fleet(self):
        unit_list = [Scout, Destroyer, Cruiser,
                     BattleCruiser, Battleship, Dreadnaught, Colonyship]
        unit_list = [
            unit for unit in unit_list if unit.req_size_tech <= self.tech.ship_size]

        planet_positions = [planet.pos for planet in self.game.planets]
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
            positions[shipyard.pos] += shipyard.tech.shipyard
        # The cheapest unit is a scout at 6 CP
        while self.construction_points >= 6:
            pos = random.choice(list(positions))
            capacity = positions[pos]
            capacity += 1
            capacity /= 2
            available_units = [unit for unit in unit_list if unit.cp_cost <=
                               self.construction_points and unit.hull_size <= capacity]
            self.build_unit(random.choice(available_units), pos)

    # Prints the player's name and unit
    def __str__(self):
        string = f"{self.name}: \n"
        for unit in self.units:
            string += str(unit)
        return string
