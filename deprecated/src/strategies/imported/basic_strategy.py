import random


class BasicStrategy:  # no movement or actual strategy, just funcitons like decide_removal or decide_which_unit_to_attack or simple_sort
    def __init__(self, player_index):  # wutever we need):
        self.player_index = player_index

    def decide_removal(self, game_state):
        return self.simple_sort(game_state)[-1]['ID']

    def decide_which_unit_to_attack(self, combat_state, coords, attacker_index):
        return next(index for index, ship in enumerate(combat_state[coords]) if self.player_index != ship['player'])

    def decide_which_units_to_screen(self, combat_state):
        return []

    def simple_sort(self, game_state):
        fixed_arr = []
        for ship_attributes in game_state['players'][self.player_index]['units']:
            if ship_attributes['type'] != 'Decoy' and ship_attributes['type'] != 'Colony Ship' and ship_attributes['type'] != 'Miner' and ship_attributes['type'] != 'Colony':
                fixed_arr.append(ship_attributes)
        sorted_arr = []
        while len(fixed_arr) > 0:
            sorted_arr.append(self.max_value(game_state, fixed_arr))
            fixed_arr.remove(self.max_value(game_state, fixed_arr))
        return sorted_arr

    def max_value(self, game_state, arr):
        strongest_ship = arr[0]
        for ship in arr[1:]:
            if self.ship_1_fires_first(game_state, ship, strongest_ship):
                strongest_ship = ship
        return strongest_ship

    def ship_1_fires_first(self, game_state, ship_1, ship_2):
        if ship_1['technology']['tactics'] > ship_2['technology']['tactics']:
            return True
        elif ship_1['technology']['tactics'] < ship_2['technology']['tactics']:
            return False
        else:
            if ship_1['technology']['attack'] > ship_2['technology']['attack']:
                return True
            elif ship_1['technology']['attack'] < ship_2['technology']['attack']:
                return False
            else:
                if game_state['unit_data'][ship_1['type']]['attack'] > game_state['unit_data'][ship_2['type']]['attack']:
                    return True
                elif game_state['unit_data'][ship_2['type']]['attack'] > game_state['unit_data'][ship_1['type']]['attack']:
                    return False
                else:
                    return True

    def strongest_enemy_ship(self, combat_state_ship_list):
        for index, unit_information in enumerate(combat_state_ship_list):
            if unit_information['player'] != self.player_index + 1:
                return index

    def decide_ship_movement(self, unit_index, game_state):
        ship_yards = game_state['players'][self.player_index]['shipyards']
        random_ship_yard = random.randint(1, len(ship_yards)) - 1
        return ship_yards[random_ship_yard]['coords'][0], ship_yards[random_ship_yard]['coords'][1]

    def will_colonize_planet(self, coordinates, game_state):
        return False

    def upgrade_costs(self, stat_to_upgrade, game_state):
        if stat_to_upgrade != 'movement':
            return game_state['technology_data'][stat_to_upgrade][game_state['players'][self.player_index]['technology'][stat_to_upgrade] - 1]
        else:
            return game_state['technology_data'][stat_to_upgrade][sum(game_state['players'][self.player_index]['technology'][stat_to_upgrade]) - 2]

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
