class Strategy:
    '''THIS CLASS IS FOR DOCUMENTATION ONLY. DO NOT CREATE SUBCLASSES OF THIS CLASS, AS IT WILL DO NOTHING.'''

    def __init__(self, player_index):
        '''
        Here, you can initialize any variables you want.
        The index of the player is passed in, so in the gamestate you can access the player.
        '''
        pass

    def will_colonize_planet(self, pos, game_state):
        '''
        This function is called whenever a colonyship moves onto a space with a planet
        You have to return either true or false.
        '''
        pass

    def decide_ship_movement(self, unit_index, game_state):
        '''
        This function is for deciding where a specific ship moves.
        You are given the unit index, which you can then access the unit from the gamestate
        Then, you must return a valid *translation* for the unit, as a tuple of the format
        (x, y)
        '''
        pass

    def decide_purchases(self, game_state):
        '''
        This function is for deciding which units and technologies to buy during the economic phase.
        You are provided with the game state.
        The output format is a dictionary formatted like so:
        {
            'technology': [
                '(tech name)',
                '(another tech name)'
            ],
            'units: [
                {
                    'type': '(unit type string)',
                    'coords': '(coords of shipyard/colony)'
                }
            ]
        }
        '''
        pass

    def decide_which_unit_to_attack(self, combat_state, coords, attacker_index):
        '''
        This function is utilised by the combat state to determine battles.
        When it is your unit's turn to attack, you are given a combat state (similar to game state), the coords,
        and the index of the attacker.
        You need to return the index of the unit you want to attack.
        '''
        pass

    def decide_removal(self, game_state):
        '''
        When you can't afford maintenance for all your ships, you must remove them.
        This function is called until you have enough cp to pay maintenance
        You must return the index of the ship you would like to destroy
        '''
        pass

    def decide_which_units_to_screen(self, combat_state):
        '''
        When you have more units than the other player in battle, you can screen your units.
        Return a list of the unit indices that you would like to screen.
        (Not implemented yet.)
        '''
        pass
