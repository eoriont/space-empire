import random
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from Player import Player
from Planet import Planet
from Unit.Colony import Colony


class Game:
    # Initialize with 2 players and turn starts at 0
    def __init__(self, grid_size, logging=False, rendering=False):
        self.current_turn = 0
        self.grid_size = grid_size
        self.logging = logging
        self.rendering = rendering
        self.players = [Player("Player 1", (3, 6), self, "blue"),
                        Player("Player 2", (3, 0), self, "red")]
        self.player_count = len(self.players)
        self.init_planets([Planet((3, 6)), Planet((3, 0))])
        self.unit_grid = self.create_unit_grid()

    # Create 8 additional randomly placed planets in addition to defaults
    def init_planets(self, planets):
        while len(planets) < 8:
            planet = random.randint(
                0, self.grid_size[0]-1), random.randint(0, self.grid_size[1]-1)
            planet = Planet(planet)
            if planet not in planets:
                planets.append(planet)
        self.planets = planets

    # Moves the player whose turn it is' units
    def complete_turn(self):
        current_player = self.players[self.current_turn % self.player_count]
        if self.logging:
            print(current_player.name)
        for unit in current_player.units:
            unit.move(random.choice(unit.get_possible_spots()))
        self.current_turn += 1
        self.unit_grid = self.create_unit_grid()

    # Create a dictionary of all the positions with multiple units on them
    def create_unit_grid(self):
        grid = {}
        units = [unit for player in self.players for unit in player.units]
        for unit in units:
            if unit.pos in grid.keys():
                grid[unit.pos].append(unit)
            else:
                grid[unit.pos] = [unit]
        return grid

    # Test for unit collisions
    def resolve_combat(self):
        combats = 0
        for _, units in self.unit_grid.items():
            if len(units) > 1:
                if [unit.player for unit in units].count(units[0].player) != len(units):
                    combats += 1
                    self.unit_battle(units)

    # Return if all the units in the given list belong to the same player
    def units_on_same_team(self, units):
        players = [unit.player for unit in units if unit.alive]
        return players.count(players[0]) == len(players)

    def sort_units_by_player(self, units):
        new_units = {}
        for unit in units:
            if name := unit.player.name in new_units.keys():
                new_units[name].append(unit)
            else:
                new_units[name] = [unit]
        return new_units

    # If units collide, fight it out
    def unit_battle(self, units):
        units = sorted(units, key=lambda x: ord(x.attack_class))
        player_units = self.sort_units_by_player(units)
        player_units = {player: len(us) for player, us in player_units.items()}
        # If a player has more units than the other, screen
        if list(player_units.values()).count(player_units[0]) != len(player_units):
            player_with_more_units = player_units.index(
                max(list(player_units.values())))
            num_units_to_screen = random.randint(
                player_units[0], player_units[1])
            units_to_screen = random.sample(
                player_units[player_with_more_units])
            for u in units_to_screen:
                units.remove(u)
        # Loop through units in the correct attack order and battle
        while not self.units_on_same_team(units):
            for unit in units:
                attack_options = [u for u in units if u.player !=
                                  unit.player and u.alive]
                if len(attack_options) == 0 or not unit.alive:
                    continue
                unit2 = random.choice(attack_options)
                u1_atk_str = unit.attack_strength + unit.tech.attack
                u2_def_str = unit2.defense_strength + unit2.tech.defense
                hit_threshold = u1_atk_str - u2_def_str
                die_roll = random.randint(0, 6)
                if die_roll <= hit_threshold or die_roll == 1:
                    unit2.hurt()
                    if self.logging:
                        print(unit2.name + " has been hurt by " + unit.name)

    # Run for 100 turns or until all of a player's units are dead
    def run_until_completion(self):
        for _ in range(self.current_turn, 100):
            self.player_upgrades()
            self.complete_turn()
            self.resolve_combat()
            if self.rendering:
                self.render_game()
            if self.winning_player() is not None:
                break
        winner = self.winning_player()
        if winner is None:
            print(self)
            print("Nobody won!")
        else:
            print("We have a winner!!")
            print("Turns taken:", self.current_turn)
            print(winner)

    # Make the choice to upgrade a technology or build a ship
    def player_upgrades(self):
        for player in self.players:
            income_list = [
                unit.cp_capacity for unit in player.units if type(unit) == Colony]
            player.pay(sum(income_list))
            player.pay_maitenance_costs()
            choice = random.randint(0, 1)
            if choice == 0:
                player.upgrade_tech()
            elif choice == 1:
                player.build_fleet()

    # Return the player who has units if someone else doesn't
    def winning_player(self):
        losers = []
        for player in self.players:
            if len(player.units) == 0:
                losers.append(player)
        winners = list(set(self.players) - set(losers))
        if len(winners) == 1:
            return winners[0]
        else:
            return None

    # Check if a position is within the game grid
    def is_in_bounds(self, x, y):
        return (x >= 0 and x < self.grid_size[0]-1) and (y >= 0 and y < self.grid_size[1]-1)

    # Prints all the players
    def __str__(self):
        string = "Game State: \n"
        for p in self.players:
            string += str(p) + "\n"
        return string

    # Make a graph of the game
    def render_game(self):
        _, ax = plt.subplots()
        ax.xaxis.set_minor_locator(MultipleLocator(.5))
        ax.yaxis.set_minor_locator(MultipleLocator(.5))

        plt.title(''.join(
            [f"| {player.name}: {player.construction_points}CP |" for player in self.players]))

        for planet in self.planets:
            plt.gca().add_patch(plt.Circle(planet.pos, radius=.5, fc='g'))

        for pos, units in self.unit_grid.items():
            x, y = pos
            for i, unit in enumerate(units):
                offset = i/len(units)
                ax.text(x, y+offset, unit.name, fontsize=12, color=unit.player.color,
                        horizontalalignment='center', verticalalignment='center')

        x_max, y_max = self.grid_size
        plt.xlim(-0.5, x_max-0.5)
        plt.ylim(-0.5, y_max-0.5)

        plt.grid(which='minor')
        plt.show()
