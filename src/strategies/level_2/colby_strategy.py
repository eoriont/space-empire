import random
import math

class BasicStrategy:  # no movement or actual strategy, just funcitons like decide_removal or decide_which_unit_to_attack or simple_sort
    def __init__(self, player_index):  # wutever we need):
        self.player_index = player_index

    def decide_removal(self, hidden_game_state):
        return self.simple_sort(hidden_game_state['players'][self.player_index]['units'])[-1]['ID']

    def decide_which_unit_to_attack(self, hidden_game_state_for_combat, combat_state,  coords, attacker_index):
        return next(index for index, ship in enumerate(combat_state[coords]) if self.player_index != ship['player'])

    def decide_which_units_to_screen(self, hidden_game_state_for_combat):
        return []

    def simple_sort(self, game_state):
        fixed_arr = []
        for ship_attributes in game_state['players'][self.player_index]['units']:
            if ship_attributes['type'] != 'Decoy' and ship_attributes['type'] != 'Colony Ship' and ship_attributes['type'] != 'Miner' and ship_attributes['type'] != 'Colony':
                fixed_arr.append(ship_attributes)
        sorted_arr = []
        while len(fixed_arr) > 0:
            strongest_ship = max(fixed_arr, key=lambda ship: ship['technology']['tactics'] + ship['technology']['tactics'] + game_state['unit_data'][ship['type']]['attack'])
            sorted_arr.append(strongest_ship)
            fixed_arr.remove(strongest_ship)
        return sorted_arr

    def decide_ship_movement(self, unit_index, game_state):
        ship_yards = game_state['players'][self.player_index]['shipyards']

        random_ship_yard = math.floor(len(ship_yards)*random.random()) + 1
        return ship_yards[random_ship_yard]['coords'][0], ship_yards[random_ship_yard]['coords'][1]

    def will_colonize_planet(self, coordinates, game_state):
        return False

    def upgrade_costs(self, stat_to_upgrade, game_state):
        return game_state['technology_data'][stat_to_upgrade][game_state['players'][self.player_index]['technology'][stat_to_upgrade]]

    def get_movement_tech(self, ship_movement_level):
        if ship_movement_level == 1:
            return [1,1,1]
        elif ship_movement_level == 2:
            return [1,1,2]
        elif ship_movement_level == 3:
            return [1,2,2]
        elif ship_movement_level == 4:
            return [2,2,2]
        elif ship_movement_level == 5:
            return [2,2,3]
        elif ship_movement_level == 5:
            return [2,3,3]


class ColbyStrategyLevel2(BasicStrategy):
    def __init__(self, player_index):  # wutever else we need):
        self.player_index = player_index
        self.__name__ = 'ColbyStrategyLevel2'

    def decide_purchases(self, hidden_game_state):
        purchases = {'units': [], 'technology': []}
        total_cost = 0
        while hidden_game_state['players'][self.player_index]['cp'] >= total_cost+6:
            purchases['units'].append({'type': 'Scout', 'coords': hidden_game_state['players'][self.player_index]['home_coords']})
            total_cost += 6
        return purchases

    def decide_ship_movement(self, unit_index, hidden_game_state):
        myself = hidden_game_state['players'][self.player_index]
        opponent = hidden_game_state['players'][1 - self.player_index]
        unit = myself['units'][unit_index]
        x_unit, y_unit = unit['coords']
        x_opp, y_opp = opponent['home_coords']
        if hidden_game_state['turn'] < 5:
            return (0,0)
        else:
            translations = [(0,0), (1,0), (-1,0), (0,1), (0,-1)]
            best_translation = (0,0)
            smallest_distance_to_opponent = 999999999999
            for translation in translations:
                delta_x, delta_y = translation
                x = x_unit + delta_x
                y = x_unit + delta_y
                dist = abs(x - x_opp) + abs(y - y_opp)
                if dist < smallest_distance_to_opponent:
                    best_translation = translation
                    smallest_distance_to_opponent = dist
            return best_translation
