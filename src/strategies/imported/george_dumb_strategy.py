from units.scout import Scout
from units.cruiser import Cruiser
from units.colonyship import Colonyship
from units.colony import Colony
from planet import Planet
from units.shipyard import Shipyard
from units.base import Base
from units.destroyer import Destroyer


class DumbStrategy:

    def __init__(self, player_num):
        self.player_num = player_num

    def decide_ship_movement(self, ship_index, game_state):
        if game_state['players'][self.player_num]['units'][ship_index]['name'] == 'Scout':
            return [-1, 0]
        else:
            return [0, 0]

    def decide_purchases(self, player_state):
        purchases = {}
        cp = player_state['cp']
        units = []
        if cp > Scout.cost:
            while True:
                if cp >= Scout.cost:
                    units.append(Scout)
                    cp -= Scout.cost
                else:
                    break
        if len(units) >= 1:
            purchases['ships'] = units
        return purchases

    def decide_removals(self, player_state):
        removals = []
        threshold = self.get_maintenance() - self.cp
        for unit in player_state['units']:
            removals.append(unit['unit num'])
            threshold -= unit['maint']
            if threshold <= 0:
                break
        return removals

    def decide_which_ship_to_attack(self, attacker, unit_info):
        return unit_info[0]

    def will_colonize(self, colony_ship, game_state):
        return False
