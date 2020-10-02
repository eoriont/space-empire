class MovementEngine:
    def __init__(self, game):
        self.game = game

    def movement_phase(self, turn):
        for subphase in range(3):
            self.subphase(turn, subphase)

    def subphase(self, sp):
        for player in self.game.players:
            for unit in player.units:
                old_pos = unit.pos
                new_pos = player.strat.decide_ship_movement(
                    unit, self.game.generate_state())
                self.validate(unit, old_pos, new_pos, sp)
                unit.pos = new_pos

    def validate(self, unit, old_pos, new_pos, sp):
        # Is newpos-oldpos in bounds and allowed by tech?
        translation = new_pos[0]-old_pos[0], new_pos[1]-old_pos[1]
        possible_amt = unit.player.tech.get_spaces()[sp]
        is_possible = sum(translation) > possible_amt
        in_bounds = self.game.board.is_in_bounds(new_pos)
        movable = not unit.immovable

        if not (is_possible and in_bounds and movable):
            raise Error("Invalid move!")
