from unit.decoy import Decoy
from unit.base import Base
from unit.ship_yard import ShipYard
from unit.colony import Colony
from unit.colony_ship import Colonyship
from unit.dreadnaught import Dreadnaught
from unit.battleship import Battleship
from unit.battle_cruiser import BattleCruiser
from unit.cruiser import Cruiser
from unit.destroyer import Destroyer
from unit.scout import Scout
from unit.unit import Unit
import sys
import random
sys.path.append('src')


class BasicStrategy:  # no movement or actual strategy, just funcitons like decide_removal or decide_which_unit_to_attack or simple_sort
    def __init__(self, player_index):  # wutever we need):
        self.player_index = player_index

    def decide_removal(self, game_state):
        sorted_list = self.simple_sort(
            game_state['players'][self.player_index]['ships'])
        total_cost = sum([ship['cost'] for ship in sorted_list])
        if total_cost > game_state['players'][self.player_index]['creds']:
            return sorted_list[-1]['id'] - 1

    def decide_which_unit_to_attack(self, full_combat_state, attacker_index, location):
        return self.strongest_enemy_ship(full_combat_state[location])

    def decide_which_units_to_screen(self, combat_state):
        return []

    def simple_sort(self, ship_dict):
        fixed_arr, sorted_arr = [], []
        for _, ship_attributes in ship_dict.items():
            if ship_attributes['name'] != 'Decoy' and ship_attributes['name'] != 'Colony Ship' and ship_attributes['name'] != 'Miner' and ship_attributes['name'] != 'Colony':
                fixed_arr.append(ship_attributes)
        while len(fixed_arr) > 0:
            sorted_arr.append(self.max_value(fixed_arr))
            fixed_arr.remove(self.max_value(fixed_arr))
        return sorted_arr

    def max_value(self, arr):
        strongest_ship = arr[0]
        for ship in arr[1:]:
            if self.ship_1_fires_first(ship, strongest_ship):
                strongest_ship = ship
        return strongest_ship

    def ship_1_fires_first(self, ship_1, ship_2):
        if ship_1['fighting_class'] > ship_2['fighting_class']:
            return True
        elif ship_1['fighting_class'] < ship_2['fighting_class']:
            return False
        else:
            if ship_1['attack_tech'] > ship_2['attack_tech']:
                return True
            elif ship_1['attack_tech'] < ship_2['attack_tech']:
                return False
            else:
                if ship_1['attack'] > ship_2['attack']:
                    return True
                elif ship_1['attack'] < ship_2['attack']:
                    return False
                else:
                    return True

    def strongest_enemy_ship(self, combat_state_ship_list):
        # unit information is {'player':M, 'unit': N}
        for unit_information in combat_state_ship_list:
            if unit_information['player'] != self.player_index:
                return unit_information['unit']

    def decide_ship_placement(self, game_state):
        return game_state['players'][self.player_index]['ship_yards']['Ship Yard', random.randint(1, len(game_state['players'][self.player_index]['ship_yards']))]['x'], game_state['players'][self.player_index]['ship_yards']['Ship Yard', random.randint(1, len(game_state['players'][self.player_index]['ship_yards']))]['y']

    def will_colonize_planet(self, game_state):
        return False
