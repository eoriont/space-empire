from technology import Technology
from unit.scout import Scout
from unit.colony_ship import Colonyship
from unit.colony import Colony
from unit.ship_yard import ShipYard


class Player:
    # Initialize player and build fleet
    def __init__(self, name, starting_pos, game, color="black"):
        self.starting_pos = starting_pos
        self.name = name
        self.units = []
        self.color = color
        self.game = game
        self.tech = Technology(
            {'atk': 0, 'def': 0, 'mov': 1, 'syc': 1, 'ss': 1})
        self.construction_points = 20
        self.build_starting_fleet()

    # Build all the ships the player starts with
    def build_starting_fleet(self):
        for _ in range(3):
            self.build_unit(Scout, pay=False)

        for _ in range(3):
            self.build_unit(Colonyship, pay=False)

        for _ in range(4):
            self.build_unit(ShipYard, pay=False)

        self.build_unit(Colony, pay=False)

    # Give the player a specified amount of cp
    def pay(self, construction_points):
        self.construction_points += construction_points

    # Pay the maintenance cost of each unit
    def pay_maintenance_costs(self):
        units_to_pay = [u for u in self.units if not u.no_maintenance]
        for unit in units_to_pay:
            cost = unit.maintenance_cost
            if self.construction_points >= cost:
                self.pay(-cost)
            else:
                self.game.log(
                    f"Unit {unit.name} was destroyed because of lack of maintenance!")
                unit.destroy()

    # Add unit to player's unit list
    def build_unit(self, unit_type, starting_pos=None, pay=True):
        starting_pos = self.starting_pos if starting_pos is None else starting_pos
        unit_name = f"{unit_type.abbr}{len(self.units)+1}"
        unit = unit_type(self, unit_name, starting_pos, self.game, self.tech)
        if pay:
            self.pay(-unit.cp_cost)
            self.game.log(
                f"{self.name} bought a {unit_type.__name__}, leaving them with {self.construction_points} cp!")
        self.units.append(unit)
        return unit

    # For each colony, pay the player their cp_capacity
    def get_income(self):
        self.pay(sum(unit.cp_capacity for unit in self.units if type(unit) == Colony))

    # Prints the player's name and units
    def __str__(self):
        string = f"{self.name}: \n"
        for unit in self.units:
            string += '    ' + str(unit)
        return string
