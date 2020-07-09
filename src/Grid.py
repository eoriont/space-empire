from Planet import Planet
import random
from Unit.Colony import Colony
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


class Grid:
    def __init__(self, game, size):
        self.grid = {}
        self.size = size
        self.game = game
        self.planets = []

    # Create a dictionary of all the positions with multiple units on them
    def create(self):
        grid = {}
        units = [
            unit for player in self.game.players for unit in player.units if unit.alive]
        for unit in units:
            if unit.pos in grid.keys():
                grid[unit.pos].append(unit)
            else:
                grid[unit.pos] = [unit]
        self.grid = grid

    # Return if all the units in the given list belong to the same player
    @staticmethod
    def units_on_same_team(units):
        players = [
            unit.player for unit in units if unit.alive and not unit.no_attack]
        if len(players) == 0:
            return True
        return players.count(players[0]) == len(players)

    # Return dictionary of players and their units in a unit list
    @staticmethod
    def sort_units_by_player(units):
        new_units = {}
        for unit in units:
            if unit.player.name in new_units.keys():
                new_units[unit.player.name].append(unit)
            else:
                new_units[unit.player.name] = [unit]
        return new_units

    # Check if a position is within the grid
    def is_in_bounds(self, x, y):
        x1, y1 = self.size
        return (x >= 0 and x < x1-1) and (y >= 0 and y < y1-1)

    # Make a graph of the game
    def render(self):
        _, ax = plt.subplots()
        ax.xaxis.set_minor_locator(MultipleLocator(.5))
        ax.yaxis.set_minor_locator(MultipleLocator(.5))

        plt.title(''.join(
            [f"| {player.name}: {player.construction_points}CP |" for player in self.game.players]))

        for planet in self.planets:
            plt.gca().add_patch(plt.Circle(planet.pos, radius=.5, fc='g'))

        for pos, units in self.items():
            x, y = pos
            for i, unit in enumerate(units):
                offset = i/len(units)
                ax.text(x, y+offset, unit.name, fontsize=12, color=unit.player.color,
                        horizontalalignment='center', verticalalignment='center')

        x_max, y_max = self.size
        plt.xlim(-0.5, x_max-0.5)
        plt.ylim(-0.5, y_max-0.5)

        plt.grid(which='minor')
        plt.show()

    # Create 8 additional randomly placed planets in addition to defaults
    def init_planets(self, *planets):
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
        unoccupied = Colony not in [type(unit) for unit in self.grid[pos]]
        if on_planet and unoccupied:
            print("test")
        return on_planet and unoccupied

    def __getitem__(self, pos):
        if pos in self.grid:
            return self.grid[pos]
        else:
            return []
