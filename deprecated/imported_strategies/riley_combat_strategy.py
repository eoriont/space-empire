class CombatStrategy:
    def __init__(self,player_num):
        self.player_num = player_num

    def will_colonize_planet(self,colony_ship_loc,game_state):
        return False
    
    def decide_ship_movement(self,ship_index, game_state):
        ship = game_state['players'][self.player_num]['units'][ship_index]
        if ship['coords'][0]>2:
            return (-1,0)
        elif ship['coords'][0]<2:
             return (1,0)
        elif ship['coords'][1]>2:
             return (0,-1)
        elif ship['coords'][1]<2:
             return (0,1)
        else:
            return (0,0)
    
    def decide_purchases(self,game_state):
        units = []
        tech = []
        ds = ['Destroyer',9]
        sc = ['Scout',6] 
        spawn_loc = game_state['players'][self.player_num]['home_coords']
        cp = game_state['players'][self.player_num]['cp']
        ship_size_tech = game_state['players'][self.player_num]['technology']['shipsize']
        ss = ['shipsize', ((ship_size_tech + 1)*5)]
        ship_choice = ss
        while cp >= ship_choice[1]:
            if ship_size_tech<2:
                ship_size_price = ((ship_size_tech + 1)*5)
                if cp > ship_size_price:
                    ship_size_tech+=1
                    tech.append('shipsize')
                    cp -= ship_size_price
                if ship_size_tech == 2:
                    ship_choice = ds
            else:
                if cp >= ship_choice[1]:
                    units.append({'type':ship_choice[0], 'coords':spawn_loc})
                    cp -= ship_choice[1]
                    
                    if ship_choice == ds:
                        ship_choice = sc
                    elif ship_choice == sc:
                        ship_choice = ds 
        return {'units':units,'technology':tech}
    
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