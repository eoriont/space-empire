import math


class DumbStrategy:

    # Only build scouts
    def decide_purchases(self, unit_types, cp, tech_types, player_state):
        scout_cost = unit_types["Scout"]["cp_cost"]
        amt = cp//scout_cost
        return {"units": {"Scout": amt}, "tech": []}

    # Remove x amount of scouts
    def decide_removals(self, player, money_needed):
        ships = player["units"]
        # Somehow get the scout maintenance cost
        if money_needed < 0:
            scout_cost = ships[0]["maintenance_cost"]
            amt_to_remove = -math.ceil(money_needed/scout_cost)
            return ships[:amt_to_remove-1]
        return []

    # Decide where each ship moves
    def decide_ship_movement(self, ship, is_in_bounds, tech_amt, get_possible_spots):
        x, y = ship["pos"]
        if is_in_bounds(1+x, 0+y):
            return (1, 0)
        return (0, 0)

    # Don't attack ships, should never happen
    def decide_ship_to_attack(self, ships):
        return None

    # Don't colonize planets
    def will_colonize_planet(self, pos, ship):
        return False
