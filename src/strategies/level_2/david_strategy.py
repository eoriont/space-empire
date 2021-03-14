class DavidStrategyLevel2:

    def __init__(self, player_index):
        self.player_index = player_index
        self.name = 'berserk'
        self.first_location=False

    def decide_ship_movement(self, ship_index, game_state):
        ship_coords = game_state['players'][self.player_index]['units'][ship_index]['coords']
        if game_state['turn']<2:
          target=(game_state['players'][self.player_index]['home_coords'][0]+2,game_state['players'][self.player_index]['home_coords'][1])
        else:
          target=game_state['players'][self.player_index-1]['home_coords']
        route = self.fastest_route(ship_coords, target)
        if ship_index<5:
          if len(route) > 0:
            return tuple(route[0])
          else:
            return (0,0)
        elif game_state['turn']>6:
          if len(route) > 0:
            return tuple(route[0])
          else:
            return (0,0)
        else:
          return (0,0)

    def decide_removals(self, player_state):
        return -1

    def decide_which_unit_to_attack(self, hidden_game_state_for_combat, combat_state, coords, attacker_index):
        combat_order = combat_state[coords]
        player_indices = [unit['player'] for unit in combat_order]

        opponent_index = 1 - self.player_index
        for combat_index, unit in enumerate(combat_order):
            if unit['player'] == opponent_index:
                return combat_index

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
        while(tuple(current) != goal):
            # print("check 1.02")
            direc = self.directional_input(current, goal)
            # print("check 1.03")
            route.append(direc)
            current  = [current[0] + direc[0], current[1] + direc[1]]
        return route

    def decide_purchases(self,game_state):
        return_dict={
           'units': [],
           'technology': []}
        current_cp = game_state['players'][self.player_index]['cp']
        while current_cp>=game_state['unit_data']['Scout']['cp_cost']:
          current_cp-=game_state['unit_data']['Scout']['cp_cost']
          return_dict['units'].append({'type': 'Scout', 'coords': game_state['players'][self.player_index]['home_coords']})
        return return_dict
