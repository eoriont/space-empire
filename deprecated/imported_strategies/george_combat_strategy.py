class CombatStrategy:

    def __init__(self, player_num):
        self.player_num = player_num
        self.buy_counter = 0

    def decide_ship_movement(self, ship_index, game_state):
        ship_coords = game_state['players'][self.player_num]['units'][ship_index]['coords']
        route = self.fastest_route(ship_coords, [game_state['board_size'][0]// 2, game_state['board_size'][1]// 2])
        if len(route) > 0:
            return tuple(route[0])
        else:
            return (0,0)

    def decide_purchases(self, game_state):
        purchases = {}
        cp = game_state['players'][self.player_num]['cp']
        units = []
        if game_state['players'][self.player_num]['technology']['shipsize'] < 2:
            purchases['technology'] = ['shipsize']
            cp -= 10
        else:
            purchases['technology'] = []
        unit = game_state['unit_data'][self.check_buy_counter()]
        if cp > unit['cp_cost']:
            while True:
                if cp >= unit['cp_cost']:
                    units.append({'type': self.check_buy_counter(), 'coords' : game_state['players'][self.player_num]['home_coords']})
                    cp -= unit['cp_cost']
                    self.buy_counter += 1
                else:
                    break
        purchases['units'] = units
        return purchases

    def check_buy_counter(self):
        if self.buy_counter % 2 == 0:
            return 'Destroyer'
        else:
            return 'Scout'


    def decide_removals(self, player_state):
        return -1
        
    def decide_which_unit_to_attack(self, combat_state, location, attacker_index):
        for unit in combat_state[tuple(location)]:
            if unit['player'] != combat_state[tuple(location)][attacker_index]['player']:
                return combat_state[tuple(location)].index(unit)

    def will_colonize(self, colony_ship, game_state):
        return False

    def decide_which_units_to_screen(self, combat_state):
        return []

    def directional_input(self, current, goal):
        directions = [[1, 0],[-1, 0],[0, 1],[0, -1],[0,0]]
        distances = []
        for i in range(len(directions)):
            new_loc = [current[0] + directions[i][0], current[1] + directions[i][1]]
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
            current  = [current[0] + direc[0], current[1] + direc[1]]
        return route