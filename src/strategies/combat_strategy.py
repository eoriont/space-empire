
class CombatStrategy:

    buy_destroyer = True

    # Buy all possible size tech and scouts/destroyers
    def decide_purchases(self, unit_types, cp, tech_types, player_state):
        ss_level = player_state["tech"]["ss"]
        purchases = {"tech": {}, "units": {}}
        if cp > tech_types["ss"]["price"][ss_level] and ss_level < 2:
            purchases["tech"]["ss"] = [2]
            cp -= tech_types["ss"]["price"][ss_level]
            ss_level = 2
        can_buy_destroyer = cp >= unit_types["Destroyer"][
            "cp_cost"] and ss_level >= unit_types["Destroyer"]["req_size_tech"]
        if self.buy_destroyer:
            if can_buy_destroyer:
                purchases["units"]["Destroyer"] = 1
        else:
            purchases["units"]["Scout"] = 1

        return purchases

    def decide_removals(self, player, money_needed):
        ships = player["units"]
        if money_needed < 0:
            m = 0
            s = []
            i = 0
            while m < -money_needed:
                s.append(ships[i])
                m += ships[i]["maintenance_cost"]
                i += 1
            return s

        return []

    # Move all ships closer to the center

    def decide_ship_movement(self, ship, is_in_bounds, tech_amt, get_possible_spots):
        possible_spaces = get_possible_spots(ship["pos"], tech_amt)
        distances = [dist((2, 2), pos)
                     for pos in possible_spaces]
        next_space = possible_spaces[distances.index(min(distances))]
        return next_space[0] - ship["pos"][0], next_space[1] - ship["pos"][1]

    # Choose the first unit to attack
    def decide_ship_to_attack(self, units):
        return units[0]

    # Don't screen any units
    def screen_units(self, units):
        return []

    # Don't colonize planets
    def will_colonize_planets(self, pos, ship):
        return False


def dist(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
