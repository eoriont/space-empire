class CombatStrategy:
    def __init__(self, player_num):
        self.player_num = player_num

    def will_colonize(self, colony_ship_loc, game_state):
        return False

    def decide_ship_movement(self, ship_index, game_state):
        ship = game_state['players'][self.player_num]['units'][ship_index]
        if ship['location'][0] > 2:
            return (-1, 0)
        elif ship['location'][0] < 2:
            return (1, 0)
        elif ship['location'][1] > 2:
            return (0, -1)
        elif ship['location'][1] < 2:
            return (0, 1)
        else:
            return (0, 0)

    def decide_purchases(self, game_state):
        units = []
        tech = []
        ds = ['Destroyer', 9]
        sc = ['Scout', 6]
        ship_choice = ds
        cp = game_state['players'][self.player_num-1]['cp']
        ship_size_tech = game_state['players'][self.player_num -
                                               1]['technology']['ship_size'][0]
        while cp >= ship_choice[1]:
            if ship_size_tech < 2:
                ship_size_price = ((ship_size_tech + 1)*5)
                if cp > ship_size_price:
                    ship_size_tech += 1
                    tech.append('ship_size')
                    cp -= ship_size_price
            else:
                if cp >= ship_choice[1]:
                    units.append(ship_choice[0])
                    cp -= ship_choice[1]

                    if ship_choice == ds:
                        ship_choice = sc
                    elif ship_choice == sc:
                        ship_choice = ds
        return {'units': units, 'technology': []}

    def decide_removals(self, game_state):
        i = 0
        while True:
            if game_state['players'][self.player_index]['units'][i]['location'] != None:
                return game_state['players'][self.player_index]['units'][i]['unit_num']
            else:
                i += 1

    def decide_which_unit_to_attack(self, attacking_ship_index, location, combat_state):
        for entry in combat_state[location]:
            if entry['player'] != combat_state[location][attacking_ship_index]['player']:
                return combat_state[location].index(entry)

    def decide_which_units_to_screen(self, combat_state):
        return []
