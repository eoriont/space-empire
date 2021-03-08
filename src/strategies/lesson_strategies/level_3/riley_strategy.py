class RileyStrategyLevel3:
    def __init__(self, player_index):
        self.player_index = player_index

    def decide_ship_movement(self, unit_index, hidden_game_state):
        myself = hidden_game_state['players'][self.player_index]
        opponent_index = 1 - self.player_index
        opponent = hidden_game_state['players'][opponent_index]

        unit = myself['units'][unit_index]
        x_unit, y_unit = unit['coords']
        x_home, y_home = myself['home_coords']
        x_opp, y_opp = opponent['home_coords']

        if (len([unit for unit in myself['units'] if unit['type'] == 'Shipyard']) <2 or len([unit for unit in myself['units'] if unit['technology']['attack'] == 2 and unit['technology']['defense'] == 2]) > 5) and hidden_game_state['turn'] >= 20:
            if unit['technology']['attack'] >= 1 or unit['technology']['defense'] >= 1:
                best_translation = self.best_move(unit, opponent, myself)
            else:
                best_translation = (0,0)
        else:
            best_translation = (0,0)



        return best_translation

    def best_move(self,unit, opponent, myself):
        x_unit, y_unit = unit['coords']
        x_home, y_home = myself['home_coords']
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

    def decide_which_unit_to_attack(self, hidden_game_state,combat_state, coords, attacker_index):
        # attack opponent's first ship in combat order

        combat_order = combat_state[coords]
        player_indices = [unit['player'] for unit in combat_order]

        opponent_index = 1 - self.player_index
        for combat_index, unit in enumerate(combat_order):
            if unit['player'] == opponent_index:
                return combat_index

    def decide_removal(self,game_state):
        for unit in game_state['players'][self.player_index]['units']:
            if unit['type'] == 'Scout':
                return game_state['players'][self.player_index]['units'].index(unit)

    def decide_purchases(self,game_state):
        units = []
        tech = []
        build_capacity = len([unit for unit in game_state['players'][self.player_index]['units'] if unit['type'] == 'ShipYard'])
        spawn_loc = game_state['players'][self.player_index]['home_coords']
        cp = game_state['players'][self.player_index]['cp']
        defense_tech = game_state['players'][self.player_index]['technology']['defense']
        attack_tech = game_state['players'][self.player_index]['technology']['attack']
        defense_cost = game_state['technology_data']['defense'][defense_tech]
        attack_cost = game_state['technology_data']['attack'][attack_tech]
        defense = ['defense',defense_cost,defense_tech]
        attack = ['attack',attack_cost,attack_tech]
        cheapest = [tech[1] for tech in [defense,attack]].index(min([tech[1] for tech in [defense,attack]]))
        tech_choice = [defense,attack][cheapest]
        ship_choice = ['Scout',6]
        if defense_tech == 2 and attack_tech == 2:
            full_tech = True
        else:
            full_tech = False

        if cp >= ship_choice[1] and build_capacity >= 1:
            units.append({'type':ship_choice[0], 'coords':spawn_loc})
            cp -= ship_choice[1]
            build_capacity -= 1

        if not full_tech:
            if cp >= tech_choice[1]:
                tech_choice[2]+=1
                tech.append(tech_choice[0])
                cp -= tech_choice[1]
                if tech_choice[0] == 'defense':
                    tech_choice = attack
                elif tech_choice[0] == 'attack':
                    tech_choice = defense


        if full_tech:
            while cp >= ship_choice[1] and build_capacity >= 1:
                units.append({'type':ship_choice[0], 'coords':spawn_loc})
                cp -= ship_choice[1]
                build_capacity -= 1


        return {'units':units,'technology':tech}
