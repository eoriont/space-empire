from Technology import Technology


class Unit:
    buyable = True
    armor = 0
    default_tech = Technology()
    hull_size = 0
    # Initialize the unit

    def __init__(self, player, name, starting_pos, game, technology=None):
        self.player = player
        self.name = name
        self.pos = starting_pos
        self.alive = True
        self.game = game
        technology = Technology() if technology is None else technology
        self.tech = Technology.combine_tech(self.default_tech, technology)
        self.maitenance_cost = self.hull_size
        self.possible_translations = self.get_possible_translations()

    # Call destroy on player
    def destroy(self):
        self.alive = False
        self.player.destroy_unit(self)

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
        if self.game.logging:
            print(f"{self.name}: {self.pos} -> {new_pos}")
        self.pos = new_pos

    # Return a list of the possible spots a unit could move to
    def get_possible_translations(self):
        speed = self.tech.speed + 1
        return [(x, y) for x in range(-speed, speed+1)
                for y in range(-speed, speed+1)
                if abs(x) + abs(y) <= speed]

    def get_possible_spots(self):
        x1, y1 = self.pos
        return [(x+x1, y+y1) for x, y in self.possible_translations if self.game.is_in_bounds(x+x1, y+y1)]
