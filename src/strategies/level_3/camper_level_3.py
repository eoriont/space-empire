class CamperLevel3:
    '''
    Stays at base while other person has o
    start w/ 3

    1. 3+2=5 => 5cp
    2. 5+3=8 => 2cp
    3. 8+2=10 => 2cp
    4. 10+2=12 => 0cp
    5. 12+1=13 => 2cp
    6. 13+1=14 => 1cp
    7. 14+1=15 => 0cp

    (MAX BUYING IN A ROW IS 15)
    '''

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
        i = next((i for i, x in enumerate(combat_state[coords]) if self.player_index != x['player'] and x['type'] == 'ShipYard'), None)
        if i:
            return i
        else:
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
        amt = min(sy_capacity, cp//scout_price)
        return {'technology': [], 'units': [{'type': 'Scout', 'coords': home_coords}] * amt}
