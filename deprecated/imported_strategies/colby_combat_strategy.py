import random
from strategies.basic_strategy import BasicStrategy
import sys
sys.path.append('src')


class CombatStrategy(BasicStrategy):
    def __init__(self, player_index):  # wutever else we need):
        self.player_index = player_index
        self.__name__ = 'CombatStrategy'
        self.previous_buy = 'Scout'

    def decide_purchases(self, game_state):
        purchases = {'units': [], 'technology': []}
        total_cost = 0
        while game_state['players'][self.player_index]['cp'] > total_cost:
            if game_state['turn'] == 1 and game_state['players'][self.player_index]['technology']['shipsize'] == 1 and 'shipsize' not in purchases['technology']:
                if game_state['players'][self.player_index]['cp'] > total_cost + self.upgrade_costs('shipsize', game_state):
                    purchases['technology'].append('shipsize')
                    total_cost += self.upgrade_costs('shipsize', game_state)
                else:
                    break
            else:
                ship = self.decide_ship_purchases(game_state)
                if game_state['players'][self.player_index]['cp'] > total_cost + self.ship_cost(ship, game_state):
                    purchases['units'].append(
                        {'type': ship, 'coords': game_state['players'][self.player_index]['home_coords']})
                    total_cost += self.ship_cost(ship, game_state)
                else:
                    break
        return purchases

    def ship_cost(self, ship, game_state):
        return game_state['unit_data'][ship]['cp_cost']

    def decide_ship_purchases(self, game_state):
        if self.check_previous_buy() == 'Destroyer':
            self.previous_buy = 'Scout'
            return 'Scout'
        if self.check_previous_buy() == 'Scout':
            self.previous_buy = 'Destroyer'
            return 'Destroyer'

    def check_previous_buy(self):
        if self.previous_buy == 'Scout':
            return 'Scout'
        elif self.previous_buy == 'Destroyer':
            return 'Destroyer'

    def decide_ship_movement(self, ship_index, game_state):
        center_point_x, center_point_y = game_state['board_size'][0] // 2, game_state['board_size'][1] // 2
        ship = game_state['players'][self.player_index]['units'][ship_index]
        ship_x, ship_y = ship['coords'][0], ship['coords'][1]
        x, y = 0, 0
        movement_tech = self.get_movement_tech(ship['technology']['movement'])
        if ship_x != center_point_x:
            if ship_x < center_point_x:
                x += movement_tech[game_state['round']]
            elif ship_x > center_point_x:
                x -= movement_tech[game_state['round']]
            return x, y
        if ship_y != center_point_y:
            if ship_y < center_point_y:
                y += movement_tech[game_state['round']]
            elif ship_y > center_point_y:
                y -= movement_tech[game_state['round']]
            return x, y
        return x, y
