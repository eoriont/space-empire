from technology import Technology


class Unit:
    armor = 0
    default_tech = {}
    hull_size = 0
    no_maitenance = False
    no_attack = False
    attack_class = None
    immovable = False

    # Initialize the unit
    def __init__(self, player, name, starting_pos, game, tech):
        self.player = player
        self.name = name
        self.pos = starting_pos
        self.alive = True
        self.game = game
        self.tech = Technology(self.default_tech, tech)
        self.maitenance_cost = 0 if self.no_maitenance else self.hull_size
        self.possible_translations = [self.get_possible_translations(0),
                                      self.get_possible_translations(1),
                                      self.get_possible_translations(2)]

    # Remove unit from player's list and alive = False
    def destroy(self):
        self.alive = False
        if self in self.player.units:
            self.player.units.remove(self)

    # Subtract 1 from armor
    def hurt(self):
        self.armor -= 1
        if self.armor <= 0:
            self.destroy()

    # Print the unit, name, and position
    def __str__(self):
        return f"({type(self).__name__}) {self.name}: {self.pos} \n"

    # Returns if unit is able to move to position and moves there if so
    def move(self, new_pos):
        self.game.log(
            f"    {self.__class__.__name__}: {self.pos} -> {new_pos}")
        self.pos = new_pos

    # Return a list of the possible spots a unit could move to
    def get_possible_translations(self, phase):
        speed = self.tech.get_spaces()[phase]
        return [(x, y) for x in range(-speed, speed+1)
                for y in range(-speed, speed+1)
                if abs(x) + abs(y) <= speed]

    def get_possible_spots(self, phase):
        x1, y1 = self.pos
        return [(x+x1, y+y1) for x, y in self.possible_translations[phase] if self.game.board.is_in_bounds(x+x1, y+y1)]
