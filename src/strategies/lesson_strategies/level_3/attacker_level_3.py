class AttackerLevel3:
    def __init__(self, player_index):
        self.player_index = player_index

    # Move if has 15 scouts (in a wave)
    def decide_ship_movement(self, unit_index, hidden_game_state):
        enemy = hidden_game_state['players'][1-self.player_index]
        enemy_home = enemy["home_coords"]
        player = hidden_game_state['players'][self.player_index]
        units = player["units"]
        unit = units[unit_index]

        # If self has 15 scouts, then attack
        # 15 scouts + 1 colony + 4 shipyards
        if len(units) >= 20 or unit['coords'] != player["home_coords"]:
            # Go to enemy base
            if unit['coords'] != enemy_home:
                direction = 1 if enemy_home[1] > unit['coords'][1] else -1
                return (0, direction)
        # Otherwise stay still
        return (0, 0)

    # Attack first scout
    def decide_which_unit_to_attack(self, hidden_game_state_for_combat, combat_state, coords, attacker_index):
        return next(i for i, x in enumerate(combat_state[coords]) if self.player_index != x['player'])

    # Just kill a scout if can't afford for some reason
    def decide_removal(self, hidden_game_state):
        return next(i for i, x in enumerate(hidden_game_state['players'][self.player_index]['units']) if x['type'] == 'Scout')

    # Buy all possible scouts
    def decide_purchases(self, game_state):
        scout_price = game_state['unit_data']['Scout']['cp_cost']
        player = game_state['players'][self.player_index]
        cp = player['cp']
        home_coords = game_state['players'][self.player_index]['home_coords']
        sy_capacity = len([i for i in player['units'] if i['type'] == 'ShipYard'])
        tt = player['technology']['defense']
        tt_price = game_state['technology_data']['defense'][tt]
        tech = []
        if tt < 2 and cp >= tt_price:
            tech += ['defense']
            cp -= tt_price
        amt = min(sy_capacity, cp//scout_price)
        return {'technology': tech, 'units': [{'type': 'Scout', 'coords': home_coords}] * amt}
