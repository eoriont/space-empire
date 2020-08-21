from technology import Technology
from unit.scout import Scout
from unit.colony_ship import Colonyship
from unit.colony import Colony
from unit.ship_yard import ShipYard


class Player:
    # Initialize player and build fleet
    def __init__(self, pid, name, starting_pos, game, color="black"):
        self.id = pid
        self.starting_pos = starting_pos
        self.name = name
        self.units = []
        self.color = color
        self.game = game
        self.tech = Technology(
            {'atk': 0, 'def': 0, 'mov': 1, 'syc': 1, 'ss': 1})
        self.cp = 20
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
    def pay(self, cp):
        self.cp += cp

    def unit_economics(self):
        colonyships = [u for u in self.units if type(u) == Colonyship]
        for c in colonyships:
            c.test_for_planet()

    # Pay the maintenance cost of each unit
    def pay_maintenance_costs(self):
        units_to_pay = [u for u in self.units if not u.no_maintenance]
        before_cp = self.cp
        for unit in sorted(units_to_pay, key=lambda x: x.cp_cost, reverse=True):
            cost = unit.maintenance_cost
            if self.cp >= cost:
                self.pay(-cost)
            else:
                unit.destroy("lack of maitenence")
        self.game.log(
            f"{self.name} payed {before_cp-self.cp} for maintenance, leaving them at {self.cp} CP")

    # Add unit to player's unit list
    def build_unit(self, unit_type, starting_pos=None, pay=True):
        starting_pos = self.starting_pos if starting_pos is None else starting_pos
        unit_name = f"P{self.id}{unit_type.abbr}{len(self.units)+1}"
        unit = unit_type(self, unit_name, starting_pos, self.game, self.tech)
        if pay:
            self.pay(-unit.cp_cost)
            self.game.log(
                f"{self.name} bought a {unit_type.__name__}, leaving them with {self.cp} cp!")
        self.units.append(unit)
        return unit

    # For each colony, pay the player their cp_capacity
    def get_income(self):
        before_cp = self.cp
        self.pay(sum(unit.cp_capacity for unit in self.units if type(unit) == Colony))
        self.game.log(
            f"{self.name} got {self.cp-before_cp} income, leaving them at {self.cp} CP!")

    def buy_tech(self, tech_type):
        price = self.tech.buy_tech(tech_type)
        self.cp -= price
        self.game.log(
            f"{self.name} bought {tech_type} for {price}, leaving them with {self.cp} CP")

    # Prints the player's name and units
    def __str__(self):
        string = f"{self.name}: \n"
        for unit in self.units:
            string += '    ' + str(unit)
        return string
