from technology import Technology
from unit import Scout, ColonyShip, Colony, ShipYard


class Player:
    # Initialize player and build fleet
    def __init__(self, strat, name, starting_pos, game):
        self.strat = strat
        self.starting_pos = starting_pos
        self.name = name
        self.units = {}
        self.game = game
        self.tech = Technology(
            {'attack': 0, 'defense': 0, 'movement': 1, 'shipyard': 1, 'shipsize': 1})
        self.cp = 0

    def start(self):
        self.build_starting_fleet()

    # Build all the ships the player starts with
    def build_starting_fleet(self):
        for _ in range(3):
            self.build_unit(Scout, free=True)

        for _ in range(3):
            self.build_unit(ColonyShip, free=True)

        for _ in range(4):
            self.build_unit(ShipYard, free=True)

        self.build_unit(Colony, free=True, unit_options={"home_colony": True})

    # Give the player a specified amount of cp
    def pay(self, cp):
        self.cp += cp

    # Get the maintenance costs for all units
    def get_maintenance(self):
        return sum(u.maintenance_cost for u in self.get_units() if not u.no_maintenance and u.alive)

    def get_units(self):
        return self.units.values()

    # Add unit to player's unit list
    def build_unit(self, unit_type, starting_pos=None, free=False, unit_options=None):
        uid = self.game.next_id()

        unit_options = {} if unit_options is None else unit_options
        starting_pos = self.starting_pos if starting_pos is None else starting_pos
        unit_name = f"P{self.id}{unit_type.abbr}{len(self.units)+1}"

        #! Should probably copy the tech instead of pointer
        unit = unit_type(uid, self, unit_name, starting_pos,
                         self.game, self.tech, **unit_options)

        # This is just for creating the starting units
        if not free:
            self.pay(-unit.cp_cost)

        self.units[uid] = unit
        return unit

    # For each colony, pay the player their cp_capacity
    def get_income(self):
        amt_to_pay = sum((20 if c.is_home_colony else c.cp_capacity)
                         for c in self.get_units()
                         if type(c) == Colony)
        return amt_to_pay

    def buy_tech(self, tech_type):
        price = self.tech.buy_tech(tech_type)
        self.cp -= price
        return price

    def get_home_coords(self):
        return next(x for x in self.get_units() if type(x) == Colony and x.is_home_colony).pos

    def get_name(self):
        return f"Player {self.id}"

    def generate_state(self):
        return {
            'cp': self.cp,
            'id': self.id,
            'units': [u.generate_state() for u in self.get_units()],
            'technology': self.tech.tech.copy(),
            'home_coords': self.get_home_coords()
        }
