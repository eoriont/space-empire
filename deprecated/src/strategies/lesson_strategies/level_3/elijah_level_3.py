class ElijahLevel3:
    # Sends a barrage of scouts towards enemy
    # While attempting to attack shipyards first

    def __init__(self, player_index):
        self.player_index = player_index
        self.priorities = ["Colony", "ShipYard", "Scout"]

    def decide_ship_movement(self, unit_index, hidden_game_state):
        enemy = hidden_game_state['players'][1-self.player_index]
        enemy_home = enemy["home_coords"]
        units = hidden_game_state['players'][self.player_index]["units"]
        unit = units[unit_index]

        # Go to enemy base
        if unit['coords'] != enemy_home:
            direction = 1 if enemy_home[1] > unit['coords'][1] else -1
            return (0, direction)

        # Otherwise stay still
        return (0, 0)

    # Attack shipyards first, then scouts
    def decide_which_unit_to_attack(self, hidden_game_state_for_combat, combat_state, coords, attacker_index):
        units = [(i, x['id']) for i, x in enumerate(combat_state[coords]) if x['player'] != self.player_index]
        opponent_units = hidden_game_state_for_combat['players'][1-self.player_index]['units']
        units = [(j, next(x for x in opponent_units if x['id'] == i)) for j, i in units]
        return min(units, key=lambda x: self.priorities.index(x[1]['type']))[0]

    # Buy all possible scouts
    def decide_purchases(self, game_state):
        scout_price = game_state['unit_data']['Scout']['cp_cost']
        player = game_state['players'][self.player_index]
        cp = player['cp']
        home_coords = game_state['players'][self.player_index]['home_coords']
        sy_capacity = len([i for i in player['units'] if i['type'] == 'ShipYard'])
        amt = min(sy_capacity, cp//scout_price)
        return {'technology': [], 'units': [{'type': 'Scout', 'coords': home_coords}] * amt}
