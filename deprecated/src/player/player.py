from technology import Technology
from unit import Scout, ColonyShip, Colony, ShipYard


class Player:
    # Initialize player and build fleet
    def __init__(self, strat, name, starting_pos, game):
        self.strat = strat
        self.starting_pos = starting_pos
        self.home_coords = starting_pos
        self.name = name
        self.units = {}
        self.game = game
        self.tech = Technology(
            {'attack': 0,
             'defense': 0,
             'movement': 1,
             'shipyard': 1,
             'shipsize': 1,
             'terraform': 0, # Unimplemented
             'tactics': 0})  # Unimplemented
        self.cp = 0 if self.state["game_level"] != 2 else 10
        self.unit_nums = {}

    def start(self):
        self.build_starting_fleet()

    # Build all the ships the player starts with
    def build_starting_fleet(self):
        for _ in range(3):
            self.build_unit(Scout, free=True)

        if self.state["game_level"] > 1:
            for _ in range(4):
                self.build_unit(ShipYard, free=True)

            if self.state["game_level"] > 3:
                for _ in range(3):
                    self.build_unit(ColonyShip, free=True)

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
        if unit_type not in self.unit_nums:
            self.unit_nums[unit_type] = 0
        self.unit_nums[unit_type] += 1
        unit_name = self.unit_nums[unit_type]

        unit = unit_type(uid, self, unit_name, starting_pos,
                         self.game, self.tech.copy(), **unit_options)

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

    def get_name(self):
        return f"Player {self.id}"

    def generate_state(self, recipient_player=True, combat=False):
        if recipient_player:
            return {
                'cp': self.cp,
                'id': self.id,
                'units': [u.generate_state(recipient_player, combat) for u in self.get_units()],
                'technology': self.tech.tech.copy(),
                'home_world': next(x.generate_state(recipient_player, True) for x in self.get_units() if type(x) == Colony and x.is_home_colony)
            }
        else:
            return {
                'id': self.id,
                'units': [u.generate_state(recipient_player, combat) for u in self.get_units()],
                'home_world': next(x.generate_state(recipient_player, True) for x in self.get_units() if type(x) == Colony and x.is_home_colony)
            }
