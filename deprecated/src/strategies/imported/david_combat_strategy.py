class CombatStrategy:#WORKS WITH GEORGE
    def __init__(self,player_num):
        self.player_num = player_num
        self.next_buy = 'Destroyer'

    def decide_ship_movement(self,ship_index, game_state):
        if game_state['players'][self.player_num]["units"][ship_index]["coords"][1]>2:
             return (0,-1)
        elif game_state['players'][self.player_num]["units"][ship_index]["coords"][1]<2:
             return (0,1)
        else:
            return (0,0)


    def decide_purchases(self,game_state):
      return_dic = {
            'units': [],
            'technology': [] 
        }
      current_cp = game_state['players'][self.player_num]['cp']
      new_shipsize= game_state['players'][self.player_num]['technology']['shipsize']
      while current_cp>=game_state['technology_data']['shipsize'][new_shipsize-1] and game_state['players'][self.player_num]['technology']['shipsize']<2:
          current_cp-=game_state['technology_data']['shipsize'][new_shipsize-1]
          new_shipsize= new_shipsize+1
          return_dic['technology'].append('shipsize')
      if new_shipsize>=2:
        while current_cp>=game_state['unit_data'][self.next_buy]['cp_cost']:
          if self.next_buy == 'Destroyer':
            self.next_buy = 'Scout'
            current_cp-=game_state['unit_data']['Destroyer']['cp_cost']
            return_dic['units'].append({'type': 'Destroyer', 'coords': game_state['players'][self.player_num]['home_coords']})
          elif self.next_buy == 'Scout':
            self.next_buy = 'Destroyer'
            current_cp-=game_state['unit_data']['Scout']['cp_cost']
            return_dic['units'].append({'type': 'Scout', 'coords': game_state['players'][self.player_num]['home_coords']})
      return return_dic

    def will_colonize_planet(self, coordinates, game_state):
      return False

    def decide_removals(self, game_state):
      return game_state["player"][self.player_num]["unit"][0]["unit number"]-1#assuming unit number starts at 1#This would remove the oldest ship, however, need to make this more complicated to remove multiple ships, currently this needs to be run mutliple times and doesn't account for ships that have no cost to maintain.

    def decide_which_unit_to_attack(self,combat_state, coords, attacker_index):
      for ship in combat_state[coords]:
        if ship['player']!=self.player_num:
          return combat_state[coords].index(ship)
      

    def decide_which_units_to_screen(self, combat_state):
      player_count = 0
      enemy_count = 0
      screens = []
      # for ship in combat_state['order']:
      #   if ship['player']!=self.player_num:
      #     enemy_count=+1
      # for ship in combat_state['order']:
      #   if ship['player']==self.player_num:
      #     player_count=+1
      #     if player_count >= enemy_count:
      #       screens.append(combat_state['order'].index(ship))
      #i thought this was nice
      return screens