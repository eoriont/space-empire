class JustinStrategyLevel2:
    # Buys as many scouts as possible, then
    # Sends all of its units one step forward to wait for enemy
    # (exploit the defender-attacks-first rule)
    # Then, after that battle, emulate the berserker strategy

    def __init__(self, player_index):
        self.player_index = player_index

    def calc_translation_towards_opponent(self, x_unit, y_unit, x_opp, y_opp):
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


    def decide_ship_movement(self, unit_index, hidden_game_state):
        myself = hidden_game_state['players'][self.player_index]
        opponent_index = 1 - self.player_index
        opponent = hidden_game_state['players'][opponent_index]

        unit = myself['units'][unit_index]
        x_unit, y_unit = unit['coords']
        x_home, y_home = myself['home_coords']
        x_opp, y_opp = opponent['home_coords']

        if (x_unit, y_unit) == (x_home, y_home):
            return self.calc_translation_towards_opponent(x_unit, y_unit, x_opp, y_opp)
        else:
            for unit in opponent['units']:
                if unit['coords'] != (x_opp, y_opp):
                    return (0,0)

            return self.calc_translation_towards_opponent(x_unit, y_unit, x_opp, y_opp)

    def decide_which_unit_to_attack(self, hidden_game_state_for_combat, combat_state, coords, attacker_index):
        # attack opponent's first ship in combat order
        combat_order = combat_state[coords]
        player_indices = [unit['player'] for unit in combat_order]

        opponent_index = 1 - self.player_index
        for combat_index, unit in enumerate(combat_order):
            if unit['player'] == opponent_index:
                return combat_index

    # Buy all possible scouts
    def decide_purchases(self, game_state):
        myself = game_state['players'][self.player_index]

        home_coords = myself['home_coords']
        cp = myself['cp']
        cp_after_maintenance = cp - 3

        scout_price = game_state['unit_data']['Scout']['cp_cost']
        num_scouts_to_buy = cp_after_maintenance // scout_price

        return {'technology': [], 'units': [{'type': 'Scout', 'coords': home_coords}] * num_scouts_to_buy }
