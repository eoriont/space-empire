class MovementEngine:
    def __init__(self, game):
        self.game = game

    def movement_phase(self, turn):
        self.game.phase = "Movement"
        self.game.log("")
        rounds = 1 if self.state["game_level"] <= 2 else 3
        for subphase in range(rounds):
            self.game.round = subphase
            self.subphase(subphase)
        self.game.round = None

    def subphase(self, sp):
        self.game.log(f"&2Phase {sp}")
        state = self.game.generate_state(None, True)
        for player in state['players']:
            self.game.current_player_id = player['id']
            for i, unit in enumerate(player['units']):
                if not self.game.unit_str_to_class(unit['type']).immovable:
                    old_pos = unit['coords']
                    p = self.state_to_player(player)
                    translation = p.strat.decide_ship_movement(i, self.game.generate_state(player=p))
                    unit_obj = self.state_to_unit(unit)
                    if translation != (0, 0):
                        self.game.log(f"{unit_obj.get_name()} moved {old_pos} -> {self.pos_from_translation(old_pos, translation)}")
                    unit_obj.validate_and_move(translation, sp)
        self.game.board.create()

    def pos_from_translation(self, p1, pos):
        return (p1[0]+pos[0], p1[1]+pos[1])

    def state_to_player(self, p):
        return self.game.players[p['id']]

    # Turn unit + player id into class
    def state_to_unit(self, unit):
        return self.game.players[unit['player']].units[unit['id']]

    def generate_movement_state(self):
        return {'round': self.game.round}
