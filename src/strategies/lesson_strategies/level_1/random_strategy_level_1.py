import random

class RandomStrategyLevel1:
    # Sends all of its units to the right

    def __init__(self, player_index):
        self.player_index = player_index

    def decide_ship_movement(self, unit_index, hidden_game_state):
        myself = hidden_game_state['players'][self.player_index]
        unit = myself['units'][unit_index]
        x_unit, y_unit = unit['coords']

        translations = [(0,0), (1,0), (-1,0), (0,1), (0,-1)]
        board_size_x, board_size_y = hidden_game_state['board_size']
        while True:
            translation = random.choice(translations)
            delta_x, delta_y = translation
            x_new = x_unit + delta_x
            y_new = y_unit + delta_y
            if 0 <= x_new and 0 <= y_new and x_new <= board_size_x-1 and y_new <= board_size_y-1:
                return translation

    def decide_which_unit_to_attack(self, hidden_game_state_for_combat, combat_state, coords, attacker_index):
        # attack opponent's first ship in combat order

        combat_order = combat_state[coords]

        opponent_index = 1 - self.player_index
        for combat_index, unit in enumerate(combat_order):
            if unit['player'] == opponent_index:
                return combat_index
