class AttackBerserkerLevel3:
    # Buys attack tech and a scout, then
    # Sends all of its units directly towards the enemy home colony

    def __init__(self, player_index):
        self.player_index = player_index

    def decide_ship_movement(self, unit_index, hidden_game_state):
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

    def decide_which_unit_to_attack(self, hidden_game_state_for_combat, combat_state, coords, attacker_index):
        return next(i for i, x in enumerate(combat_state[coords]) if self.player_index != x['player'])

    def decid_which_units_to_screen(self, units):
        return None

    # Buys a scout and attack tech
    def decide_purchases(self, game_state):
        tech = []
        units = []
        p = game_state['players'][self.player_index]
        cp = p['cp']
        tech_cost = game_state['technology_data']['attack'][p['technology']['attack']]
        if cp >= tech_cost and tech_cost == 20:
            tech.append('attack')
            cp -= tech_cost
        elif game_state['players'][self.player_index]['cp'] >= 6:
            cp -= 6
            units.append({'type': 'Scout', 'coords': game_state['players'][self.player_index]['home_coords']})
        return {'technology': tech, 'units': units}
