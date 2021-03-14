class DumbStrategyLevel1:
    # Sends all of its units to the right

    def __init__(self, player_index):
        self.player_index = player_index

    def decide_ship_movement(self, unit_index, hidden_game_state):
        myself = hidden_game_state['players'][self.player_index]
        unit = myself['units'][unit_index]
        x_unit, y_unit = unit['coords']

        board_size_x, board_size_y = hidden_game_state['board_size']
        unit_is_at_edge = (x_unit == board_size_x-1)
        if unit_is_at_edge:
            return (0,0)
        else:
            return (1,0)

    def decide_which_unit_to_attack(self, hidden_game_state_for_combat, combat_state, coords, attacker_index):
        # attack opponent's first ship in combat order

        combat_order = combat_state[coords]
        player_indices = [unit['player'] for unit in combat_order]

        opponent_index = 1 - self.player_index
        for combat_index, unit in enumerate(combat_order):
            if unit['player'] == opponent_index:
                return combat_index
