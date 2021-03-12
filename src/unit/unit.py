from technology import Technology


class Unit:
    armor = 0
    default_tech = {}
    hull_size = 0
    no_maintenance = False
    no_attack = False
    attack_class = None
    immovable = False

    # Initialize the unit
    def __init__(self, uid, player, name, starting_pos, game, tech):
        self.name = name
        self.id = uid
        self.player = player
        self.id = uid
        self.pos = starting_pos
        self.alive = True
        self.game = game
        self.tech = Technology(self.default_tech, tech)
        self.maintenance_cost = 0 if self.no_maintenance else self.hull_size

    # Remove unit from player's list and alive = False
    def destroy(self, hurter_name=None):
        self.alive = False
        if self.id in self.player.units:
            self.game.log(f"{self.get_name()} &1has been destroyed! Reason: {hurter_name}")
            del self.player.units[self.id]
        else:
            #! Handle the offcase
            pass

    # Subtract 1 from armor
    def hurt(self, hurter_name):
        self.armor -= 1
        if self.armor <= 0:
            self.destroy(hurter_name)

    # Check if movement is valid and move if so
    def validate_and_move(self, translation, sp):
        # Is newpos-oldpos in bounds and allowed by tech?
        possible_amt = self.tech.get_spaces()[sp]
        is_possible = sum(translation) <= possible_amt
        new_pos = self.pos_from_translation(translation)
        in_bounds = self.game.board.is_in_bounds(new_pos[0], new_pos[1])
        movable = not self.immovable
        if not (is_possible and in_bounds and movable):
            self.game.throw("Invalid move!",
                f"""
&4Unit {self.id} started at &3{self.pos}
&4Unit type can move: &3{movable}
&4Tried to move from &3{self.pos} --> {new_pos}
&4In bounds: &3{in_bounds}
&4Enough movement technology: &3{is_possible}
&4Exact returned translation: &3{translation}
                """
            )
        self.pos = new_pos

    def pos_from_translation(self, pos):
        return (self.pos[0]+pos[0], self.pos[1]+pos[1])

    def generate_state(self, recipient_player=True, combat=False):
        if recipient_player or combat:
            return {
                'num': self.name,
                'coords': self.pos,
                'type': type(self).__name__,
                'hits_left': type(self).armor-self.armor,
                'technology': self.tech.get_obj_state(),
                'player': self.player.id,
            }
        else:
            return {
                'coords': self.pos,
                'player': self.player.id,
            }

    def get_name(self):
        return f"Player {self.player.id} {type(self).__name__} {self.id}"
