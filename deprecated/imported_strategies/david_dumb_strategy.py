class DumbStrategy:#WORKS WITH GEORGE
    def __init__(self,player_num):
        self.player_num = player_num

    def will_colonize_planet(self,colony_ship, game_state):
      return False

    def decide_ship_movement(self,ship_index, game_state):
        if game_state['players'][self.player_num]["units"][ship_index]["coords"][0]<game_state['board_size'][0]-1:
             return (1,0)
        else:
            return (0,0)

    def decide_purchases(self,game_state):
        return_dict={
           'units': [],
           'technology': []}
        current_cp = game_state['players'][self.player_num]['cp']
        while current_cp>=game_state['unit_data']['Scout']['cp_cost']:
          current_cp-=game_state['unit_data']['Scout']['cp_cost']
          return_dict['units'].append({'type': 'Scout', 'coords': game_state['players'][self.player_num]['home_coords']})
        return return_dict



    def decide_removal(self, game_state):
      return game_state["players"][self.player_num]["units"][0]["unit_num"]-1#assuming unit number starts at 1
  
    def decide_which_ship_to_attack(self,combat_state, coords, attacker_index):
      return None

    def decide_which_units_to_screen(self, combat_state):
      return []
