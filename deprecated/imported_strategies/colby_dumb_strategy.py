import random
from strategies.basic_strategy import BasicStrategy
import sys
sys.path.append('src')


class DumbStrategy(BasicStrategy):
    def __init__(self, player_index):  # wutever else we need):
        self.player_index = player_index
        self.__name__ = 'DumbStrategy'

    def decide_purchases(self, game_state):
        return self.decide_ship_purchases(game_state)

    def decide_ship_purchases(self, game_state):
        return {'units': [{'type': 'Scout', 'coords': game_state['players'][self.player_index]['home_coords']}] * (game_state['players'][self.player_index]['cp'] // 6), 'technology': []}

    def decide_ship_movement(self, ship_index, game_state):
        x, y = 0, 0
        movement_tech = self.get_movement_tech(
            game_state['players'][self.player_index]['units'][ship_index]['technology']['movement'])
        if game_state['players'][self.player_index]['units'][ship_index]['coords'][0] + movement_tech[game_state['round']] < game_state['board_size'][0]:
            x += movement_tech[game_state['round']]
        return x, y
