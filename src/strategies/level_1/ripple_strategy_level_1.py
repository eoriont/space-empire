class RippleStrategyLevel1:
    # Staggers the sending of all of its units directly towards the enemy home colony

    def __init__(self, player_index):
        self.player_index = player_index
        self.allowed_units = 0
        self.last_turn = 1

    def decide_ship_movement(self, unit_index, hidden_game_state):
        if hidden_game_state['turn'] != self.last_turn:
            self.last_turn = hidden_game_state['turn']
            self.allowed_units += 1
        if self.allowed_units >= unit_index:
            myself = hidden_game_state['players'][self.player_index]
            opponent_index = 1 - self.player_index
            opponent = hidden_game_state['players'][opponent_index]

            unit = myself['units'][unit_index]
            x_unit, y_unit = unit['coords']
            x_opp, y_opp = opponent['home_coords']

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
        return (0, 0)

    def decide_which_unit_to_attack(self, hidden_game_state_for_combat, combat_state, coords, attacker_index):
        # attack opponent's first ship in combat order

        combat_order = combat_state[coords]

        opponent_index = 1 - self.player_index
        for combat_index, unit in enumerate(combat_order):
            if unit['player'] == opponent_index:
                return combat_index
