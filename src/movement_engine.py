class MovementEngine:
    def __init__(self, game):
        self.game = game

    def movement_phase(self, turn):
        for subphase in range(3):
            self.subphase(subphase)

    def subphase(self, sp):
        for player in self.game.players:
            for unit in player.units:
                if not unit.immovable:
                    old_pos = unit.pos
                    translation = player.strat.decide_ship_movement(
                        player.generate_state(unit),
                        self.game.board.is_in_bounds,
                        player.tech.get_spaces()[sp],
                        self.game.board.get_possible_spots)
                    unit.validate_and_move(translation, sp)
        self.game.board.create()
