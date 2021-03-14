class DumbStrategy:
    def __init__(self,player_index):
        self.player_index = player_index

    def will_colonize_planet(self,colony_ship_loc,game_state):
        return True
    
    def decide_ship_movement(self,ship_index, game_state):
        ship = game_state['players'][self.player_index]['units'][ship_index]
        if ship['coords'][0] != game_state['board_size'][0]-1:
           return (1, 0)
        else:
            return (0,0)
    
    def decide_purchases(self,game_state):
        units = []
        spawn_coords = game_state['players'][self.player_index]['home_coords']
        money = game_state['players'][self.player_index]['cp']
        while money - 6 >= 0:
            units.append({'type':'Scout', 'coords': spawn_coords})
            money -= 6
        return {'units':units,'technology':[]}
    
    def decide_removals(self, game_state):
        i = 0
        while True:
            if game_state['players'][self.player_index]['units'][i]['alive']:
                return game_state['players'][self.player_index]['units'][i]['unit_num']
            else:
                i+=1

    def decide_which_unit_to_attack(self, combat_state, location, attacking_ship_index):
        for entry in combat_state[location]:
            if entry['player'] != combat_state[location][attacking_ship_index]['player']:
                return combat_state[location].index(entry)

    def decide_which_units_to_screen(self, combat_state):
        return []