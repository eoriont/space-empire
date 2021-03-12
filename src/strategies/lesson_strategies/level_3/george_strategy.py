class GeorgeStrategyLevel3:
    def __init__(self, player_num):
        self.player_index = player_num
        self.name = 'George'
        self.delayed_count = 0
        self.flank_count = 0
        self.flank_turn = None
        self.flank_started = False
        self.turn_count = 1
        self.movement = 1
        self.flank_route_index = 0
        self.behind_direction = {(3,0): (-1,0), (3,6): (1,0)}
        self.flank_route = {(3,0): [(0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (1,0), (0,0)],  (3,6): [(0,-1), (0,-1), (0,-1), (0,-1), (0,-1), (0,-1), (-1,0), (0,0)]}

    def decide_purchases(self, game_state):
        myself = game_state['players'][self.player_index]
        home_coords= game_state['players'][self.player_index]['home_coords']
        units = myself['units']
        scouts = [unit for unit in units if unit['type'] == 'Scout']
        shipyards = [unit for unit in units if unit['type'] == 'ShipYard']
        scouts_bought = 0
        num_units = len(scouts)
        attack_level = myself['technology']['attack']
        game_turn = game_state['turn']
        purchases = {'units': [], 'technology': []}
        if attack_level < 3 and myself['cp'] >= game_state['technology_data']['attack'][attack_level]:
            purchases['technology'].append('attack')
            myself['cp'] -= game_state['technology_data']['attack'][attack_level]
        while myself['cp'] >= 6:
            if scouts_bought == len(shipyards):
                break;
            purchases['units'].append({'type': 'Scout', 'coords': home_coords})
            myself['cp'] -= 6
            scouts_bought += 1
        return purchases

    def decide_ship_movement(self, unit_index, hidden_game_state):
        myself = hidden_game_state['players'][self.player_index]
        home_coords= tuple(hidden_game_state['players'][self.player_index]['home_coords'])
        units = myself['units']
        scouts = [unit for unit in units if unit['type'] == 'Scout' and tuple(unit['coords']) != home_coords]
        num_units = len(scouts)
        game_turn = hidden_game_state['turn']
        game_round = hidden_game_state['round']
        if game_turn != self.turn_count or self.movement != game_round:
            if self.flank_started and self.flank_route_index < 7:
                self.flank_route_index +=1
            self.turn_count = game_turn
            self.movement = game_round
            self.delayed_count = 0
        if self.flank_started and num_units == 0:
            self.flank_route_index = 0
            self.flank_started= False
            self.flank_count = 0
        opponent_index = 1 - self.player_index
        unit = myself['units'][unit_index]
        # print(unit['type'], unit['coords'], home_coords, self.flank_count, len(scouts))
        if unit['type'] == 'Scout' and self.delayed_count < 6 and tuple(unit['coords']) == home_coords:
            self.delayed_count += 1
            return (0,0)
        elif self.delayed_count >= 6 or self.flank_started:
            if tuple(unit['coords']) == home_coords:
                if self.flank_started:
                    return (0,0)
                self.flank_count += 1
                return self.behind_direction[home_coords]
            if self.flank_count >= 6:
                self.flank_turn = game_turn
                self.flank_started = True
                return self.flank_route[home_coords][self.flank_route_index]
            else:
                return (0,0)
        else:
            return (0,0)

    def decide_which_unit_to_attack(self, hidden_game_state_for_combat, combat_state, coords, attacker_index):
        # attack opponent's first ship in combat order
        combat_order = combat_state[coords]
        player_indices = [unit['player'] for unit in combat_order]
        opponent_index = 1 - self.player_index
        for combat_index, unit in enumerate(combat_order):
            if unit['player'] == opponent_index:
                return combat_index

    def decide_removal(self,game_state):
        return -1
