class FlankerStrategyLevel2:
    # Uses an upgraded movement scout to flank the other colony

    def __init__(self, player_index):
        self.player_index = player_index
        self.flank_direction = (1,0)
        self.flank_index = None

    def decide_ship_movement(self, unit_index, hidden_game_state):
        myself = hidden_game_state['players'][self.player_index]
        opponent_index = 1 - self.player_index
        opponent = hidden_game_state['players'][opponent_index]

        unit = myself['units'][unit_index]
        x_unit, y_unit = unit['coords']
        x_opp, y_opp = opponent['home_coords']

        translations = [(0,0), (1,0), (-1,0), (0,1), (0,-1)]

        if self.flank_index is None:
            if unit['type'] == 'Scout' and unit['technology']['movement'] == 1:
                self.flank_index = unit_index

        # unit 0 does the flanking
        if unit_index == self.flank_index:
            dist = abs(x_unit - x_opp) + abs(y_unit - y_opp)
            delta_x, delta_y = self.flank_direction
            reverse_flank_direction = (-delta_x, -delta_y)

            # at the start, sidestep
            if unit['coords'] == myself['home_coords']:
                return self.flank_direction

            # at the end, reverse the sidestep to get to enemy
            elif dist == 1:
                return reverse_flank_direction

            # during the journey to the opponent, don't
            # reverse the sidestep
            else:
                translations.remove(reverse_flank_direction)

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
        player_indices = [unit['player'] for unit in combat_order]

        opponent_index = 1 - self.player_index
        for combat_index, unit in enumerate(combat_order):
            if unit['player'] == opponent_index:
                return combat_index

    # Buys movement tech then a scout
    def decide_purchases(self, game_state):
        return {'technology': ['movement'], 'units': [{'type': 'Scout', 'coords': game_state['players'][self.player_index]['home_coords']}]}
