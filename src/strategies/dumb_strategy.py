import math
from strategies.strategy_util import is_in_bounds


class DumbStrategy:

    def __init__(self, player_index):
        self.player_index = player_index

    # Don't colonize planets
    def will_colonize_planet(self, pos, game_state):
        return False

    # Decide where each ship moves
    def decide_ship_movement(self, unit_index, game_state):
        x, y = game_state["players"][self.player_index]['units'][unit_index]["location"]
        if is_in_bounds(1+x, 0+y, game_state["board_size"]):
            return (1, 0)
        return (0, 0)

    # Only build scouts
    def decide_purchases(self, game_state):
        scout_cost = game_state['unit_types']["Scout"]["cp_cost"]
        amt = game_state['players'][self.player_index]['cp']//scout_cost
        return {"units": ["Scout"]*amt, "tech": {}}

    # Don't attack ships, should never happen
    def decide_which_unit_to_attack(self, combat_state, location, attacker_index):
        return None

    # Remove the first ship
    def decide_removal(self, game_state):
        return 0

    def decide_which_units_to_screen(self, combat_state):
        return []
