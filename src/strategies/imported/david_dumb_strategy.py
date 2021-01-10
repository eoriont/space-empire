class DumbStrategy:
    def __init__(self, player_num):
        self.player_num = player_num

    def will_colonize_planet(self, colony_ship, game_state):
        return False

    def decide_ship_movement(self, ship, game_state):
        if ship.coordinates[0] < 4:
            return (1, 0)
        else:
            # if theres a specific place in mind, write code for that lazy
            return (0, 0)

    def decide_purchases(self, game_state):
        # referance the "army_choices" int in player to see what number is what. IF OTHER OPTIONS, RETURN WITH A RANDOM. IF TECH COULD BE UPGRADED, IT WOULD BE LAST POSITION
        return["Unit Buy", 0]

    def decide_which_ship_to_attack(attacking_ship, game_state):
        return None
