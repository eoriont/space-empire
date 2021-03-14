
class RileyStrategyLevel2:
    def __init__(self, player_num):
        self.player_num = player_num

    def decide_ship_movement(self, unit_index, hidden_game_state):
        myself = hidden_game_state['players'][self.player_num]
        opponent_index = 1 - self.player_num

        opponent = hidden_game_state['players'][opponent_index]

        unit = myself['units'][unit_index]
        x_unit, y_unit = unit['coords']
        x_opp, y_opp = opponent['home_coords']

        if unit_index >= 9:
             best_translation = self.best_move(unit, opponent)
        else:
            if hidden_game_state['turn'] < 10:
                best_translation = (0,0)
            else:
                best_translation = self.best_move(unit, opponent)

        return best_translation

    def best_move(self,unit, opponent):
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

    def decide_which_unit_to_attack(self, hidden_game_state_for_combat, combat_state, coords, attacker_index):
        # attack opponent's first ship in combat order

        combat_order = combat_state[coords]
        player_indices = [unit['player'] for unit in combat_order]

        opponent_index = 1 - self.player_num
        for combat_index, unit in enumerate(combat_order):
            if unit['player'] == opponent_index:
                return combat_index

    def decide_purchases(self,game_state):
        units = []
        tech = []
        sc = ['Scout',6]
        spawn_loc = game_state['players'][self.player_num]['home_coords']
        cp = game_state['players'][self.player_num]['cp']
        ship_choice = sc

        while cp >= ship_choice[1]:
                units.append({'type':ship_choice[0], 'coords':spawn_loc})
                cp -= ship_choice[1]
        return {'units':units,'technology':tech}
