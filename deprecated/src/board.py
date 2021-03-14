from planet import Planet
import random
from unit import Colony, ShipYard
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


class Board:
    def __init__(self, game, size):
        self.grid = {}
        self.size = size
        self.center = [(x-1)/2 for x in size]
        self.game = game
        self.planets = []

    # Create a dictionary of all the positions with multiple units on them
    def create(self):
        grid = {}
        units = [
            unit for player in self.game.players for unit in player.get_units() if unit.alive]
        for unit in units:
            if unit.pos in grid.keys():
                grid[unit.pos].append(unit)
            else:
                grid[unit.pos] = [unit]
        self.grid = grid

    # Check if a position is within the grid
    def is_in_bounds(self, x, y):
        x1, y1 = self.size
        return (x >= 0 and x < x1) and (y >= 0 and y < y1)

    # Create 8 additional randomly placed planets in addition to defaults
    # Unless game is in simple mode, just create home colonies
    def init_planets(self, *planets):
        if self.state["game_level"] > 3:
            planets = list(planets)
            while len(planets) < 8:
                planet = random.randint(
                    0, self.size[0]-1), random.randint(0, self.size[1]-1)
                if planet not in planets:
                    planets.append(planet)
        self.planets = [Planet(p) for p in planets]

    # Return list of grid positions and unit lists
    def items(self):
        return self.grid.items()

    # Return if the pos is on an unoccupied planet
    def on_unoccupied_planet(self, pos):
        on_planet = pos in [p.pos for p in self.planets]
        unoccupied = Colony not in [type(unit) for unit in self[pos]]
        return on_planet and unoccupied

    # Return if the given position contains a certain type of ship
    def contains(self, pos, t):
        return self.game.unit_str_to_class(t) in [type(u) for u in self[pos]]

    def get_shipyard_capacity(self, pos):
        return len([x for x in self[pos] if type(x) == ShipYard])


    def __getitem__(self, pos):
        if pos in self.grid:
            return self.grid[pos]
        else:
            return []
