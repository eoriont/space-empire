class ShieldStrategyLevel2:
    # Buys as many scouts as possible, then
    # waits for opponent to attack base,
    # then attacks opponents base

    def __init__(self, player_index):
        self.player_index = player_index

    def decide_ship_movement(self, unit_index, hidden_game_state):
        enemy = hidden_game_state['players'][1-self.player_index]
        enemy_home = enemy["home_coords"]
        units = hidden_game_state['players'][self.player_index]["units"]
        unit = units[unit_index]

        # If enemy has no more scouts
        if next((i for i in enemy['units'] if i['type'] == 'Scout'), None) is None:
            # Go to enemy base
            if not unit['coords'] == enemy_home:
                direction = 1 if enemy_home[1] > unit['coords'][1] else 0
                return (0, direction)
        # Otherwise stay still
        return (0, 0)


    # attack opponent's first ship in combat order
    def decide_which_unit_to_attack(self, hidden_game_state_for_combat, combat_state, coords, attacker_index):
        return next(i for i, x in enumerate(combat_state[coords]) if self.player_index != x['player'])

    # Buy all possible scouts
    def decide_purchases(self, game_state):
        cp = game_state['players'][self.player_index]['cp']
        scout_cost = game_state['unit_data']['Scout']['cp_cost']
        return {'technology': [], 'units': [
            {'type': 'Scout', 'coords': game_state['players'][self.player_index]['home_coords']}
        ] * (cp//scout_cost)}
