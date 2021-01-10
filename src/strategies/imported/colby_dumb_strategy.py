from strategies.imported.colby_basic_strategy import BasicStrategy
from unit.carrier import Carrier
from unit.decoy import Decoy
from unit.miner import Miner
from unit.base import Base
from unit.ship_yard import Ship_Yard
from unit.colony import Colony
from unit.colony_ship import Colony_Ship
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


class DumbStrategy(BasicStrategy):
    def __init__(self, player_index):  # wutever else we need):
        self.player_index = player_index

    def decide_purchases(self, game_state):
        return self.decide_ship_purchases(game_state)

    def decide_ship_purchases(self, game_state):
        return Scout(None, (0, 0), 0, 0, True)

    def decide_ship_movement(self, ship, game_state, movement_round):
        x, y = 0, 0
        if ship['x'] < game_state['players'][self.player_index]['grid_size']:
            x += ship['movement_tech'][movement_round]
        return x, y
