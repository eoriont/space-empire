
from unit.destroyer import Destroyer
from unit.base import Base
from unit.ship_yard import ShipYard
from planet import Planet
from unit.colony import Colony
from unit.colony_ship import Colonyship
from unit.cruiser import Cruiser
from unit.scout import Scout
import sys
sys.path.append('src')


class CombatStrategy:

    def __init__(self, player_num):
        self.player_num = player_num
        self.buy_counter = 0

    def decide_ship_movement(self, ship_index, game_state):
        ship_coords = game_state['players'][self.player_num]['units'][ship_index]['coords']
        route = self.fastest_route(
            ship_coords, [game_state['board_size'][0] // 2, game_state['board_size'][1] // 2])
        if len(route) > 0:
            return route[0]
        else:
            return [0, 0]

    def decide_purchases(self, player_state):
        purchases = {}
        cp = player_state['cp']
        units = []
        if player_state['tech']['ss'] < 2:
            purchases['tech'] = [['ss', 1]]
            cp -= 10
        if cp > self.check_buy_counter().cost:
            while True:
                unit = self.check_buy_counter()
                if cp >= unit.cost:
                    units.append(unit)
                    cp -= unit.cost
                    self.buy_counter += 1
                else:
                    break
        if len(units) >= 1:
            purchases['ships'] = units
        return purchases

    def check_buy_counter(self):
        if self.buy_counter % 2 == 0:
            return Destroyer
        else:
            return Scout

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

    def directional_input(self, current, goal):
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        distances = []
        for i in range(len(directions)):
            new_loc = [current[0] + directions[i]
                       [0], current[1] + directions[i][1]]
            dist = self.distance(new_loc, goal)
            distances.append(dist)
        closest = min(distances)
        index = distances.index(closest)
        return directions[index]

    def distance(self, current, goal):
        return ((current[0] - goal[0])**2 + (current[1] - goal[1])**2)**(0.5)

    def fastest_route(self, current, goal):
        route = []
        while(current != goal):
            direc = self.directional_input(current, goal)
            route.append(direc)
            current = [current[0] + direc[0], current[1] + direc[1]]
        return route
