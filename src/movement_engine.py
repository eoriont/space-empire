class MovementEngine:
    def __init__(self, game):
        self.game = game

    def movement_phase(self, turn):
        self.game.phase = "Movement"
        for subphase in range(3):
            self.game.round = subphase
            self.subphase(subphase)
        self.game.round = None

    def subphase(self, sp):
        state = self.game.generate_state(sp=sp)
        for player in state['players']:
            for i, unit in enumerate(player['units']):
                if not unit['type'].immovable:
                    old_pos = unit['coords']
                    translation = self.state_to_player(
                        player).strat.decide_ship_movement(i, state)
                    self.state_to_unit(unit).validate_and_move(translation, sp)
        self.game.board.create()

    def state_to_player(self, p):
        return self.game.players[p['id']]

    # Turn unit + player id into class
    def state_to_unit(self, unit):
        return self.game.players[unit['player']].units[unit['id']]

    def generate_movement_state(self):
        return {'round': self.game.round}
