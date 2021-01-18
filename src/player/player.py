from technology import Technology
from unit.scout import Scout
from unit.colony_ship import Colonyship
from unit.colony import Colony
from unit.ship_yard import ShipYard


class Player:
    # Initialize player and build fleet
    def __init__(self, strat, name, starting_pos, game):
        self.strat = strat
        self.starting_pos = starting_pos
        self.name = name
        self.units = []
        self.game = game
        self.tech = Technology(
            {'attack': 0, 'defense': 0, 'movement': 1, 'shipyard': 1, 'shipsize': 1})
        self.cp = 0

    def start(self):
        self.build_starting_fleet()

    # Build all the ships the player starts with
    def build_starting_fleet(self):
        for _ in range(3):
            self.build_unit(Scout, pay=False)

        for _ in range(3):
            self.build_unit(Colonyship, pay=False)

        for _ in range(4):
            self.build_unit(ShipYard, pay=False)

        self.build_unit(Colony, pay=False, unit_options={"home_colony": True})

    # Give the player a specified amount of cp
    def pay(self, cp):
        self.cp += cp

    # Get the maintenance costs for all units
    def get_maintenance(self):
        return sum(u.maintenance_cost for u in self.units if not u.no_maintenance and u.alive)

    # Add unit to player's unit list

    def build_unit(self, unit_type, starting_pos=None, pay=True, unit_options=None):
        unit_options = {} if unit_options is None else unit_options
        starting_pos = self.starting_pos if starting_pos is None else starting_pos
        unit_name = f"P{self.id}{unit_type.abbr}{len(self.units)+1}"
        unit = unit_type(self, unit_name, starting_pos,
                         self.game, self.tech, **unit_options)
        if pay:
            self.pay(-unit.cp_cost)
        self.units.append(unit)
        return unit

    # For each colony, pay the player their cp_capacity
    def get_income(self):
        amt_to_pay = sum((20 if c.is_home_colony else c.cp_capacity)
                         for c in self.units
                         if type(c) == Colony)
        return amt_to_pay

    def buy_tech(self, tech_type):
        price = self.tech.buy_tech(tech_type)
        self.cp -= price

    def generate_state(self, unit):
        other_units = [
            unit.pos for player in self.game.players for unit in player.units if player != self]
        return {
            "pos": unit.pos,
            "unknown_units": other_units,
            "cp": self.cp
        }

    def economic_state(self):
        ships = [{
            "maintenance_cost": unit.maintenance_cost,
            "id": unit.id
        } for unit in self.units if not unit.no_maintenance]
        return {
            "units": ships,
            "tech": self.tech.tech.copy()
        }

    def get_unit_by_id(self, uid):
        return next(x for x in self.units if uid == x.id)

    def get_home_coords(self):
        return next(x for x in self.units if type(x) == Colony and x.is_home_colony).pos
