class GeorgeStrategyLevel2:
    def __init__(self, player_num):
        self.player_index = player_num
        self.name = 'delayed_nums'

    def decide_purchases(self, game_state):
        home_coords= game_state['players'][self.player_index]['home_coords']
        return {'units': [{'type': 'Scout', 'coords': home_coords}, {'type': 'Scout', 'coords': home_coords}, {'type': 'Scout', 'coords': home_coords}, {'type': 'Scout', 'coords': home_coords}], 'technology': []}

    def decide_ship_movement(self, unit_index, hidden_game_state):
        delayed_count = 0
        myself = hidden_game_state['players'][self.player_index]
        units = myself['units']

        opponent_index = 1 - self.player_index
        opponent = hidden_game_state['players'][opponent_index]

        unit = myself['units'][unit_index]
        x_unit, y_unit = unit['coords']
        x_opp, y_opp = opponent['home_coords']
        if len(opponent['units']) > 5:
            return (0,0)
        translations = [(0,0), (1,0), (-1,0), (0,1), (0,-1)]
        best_translation = (0,0)
        smallest_distance_to_opponent = 999999999999
        for translation in translations:
            delta_x, delta_y = translation
            x = x_unit + delta_x
            y = x_unit + delta_y
            dist = abs(x - x_opp) + abs(y - y_opp)
            if dist < smallest_distance_to_opponent:
                best_translation = translation
                smallest_distance_to_opponent = dist
        return best_translation

    def decide_which_unit_to_attack(self, hidden_game_state_for_combat, combat_state, coords, attacker_index):
        # attack opponent's first ship in combat order

        combat_order = combat_state[coords]

        opponent_index = 1 - self.player_index
        for combat_index, unit in enumerate(combat_order):
            if unit['player'] == opponent_index:
                return combat_index
