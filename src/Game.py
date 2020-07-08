import random
from Player import Player
from Unit.Colony import Colony
from Grid import Grid
from Unit.Decoy import Decoy


class Game:
    # Initialize with 2 players and turn starts at 0
    def __init__(self, grid_size, logging=False, rendering=False):
        self.current_turn = 0
        self.logging = logging
        self.rendering = rendering
        self.players = [Player("Player 1", (3, 6), self, "blue"),
                        Player("Player 2", (3, 0), self, "red")]
        self.player_count = len(self.players)
        self.grid = Grid(self, grid_size)
        self.grid.init_planets((3, 6), (3, 0))
        self.grid.create()

    # If units collide, fight it out
    def unit_battle(self, units):
        units = sorted(units, key=lambda x: ord(x.attack_class or 'Z'))
        player_units = Grid.sort_units_by_player(units)
        player_units_len = {player: len(us)
                            for player, us in player_units.items()}
        # If a player has more units than the other, screen
        unit_nums = list(player_units_len.values())
        if unit_nums.count(unit_nums[0]) != len(unit_nums):
            player_with_more_units = max(
                player_units_len, key=player_units_len.get)
            nums = unit_nums[:2] if unit_nums[0] < unit_nums[1] else unit_nums[:2][::-1]
            num_units_to_screen = random.randint(*nums)
            units_to_screen = random.sample(
                player_units[player_with_more_units], num_units_to_screen)
            for u in units_to_screen:
                units.remove(u)
        for u in units:
            if type(u) == Decoy:
                u.destroy()
                units.remove(u)
        # Loop through units in the correct attack order and battle
        while not Grid.units_on_same_team(units):
            for unit in units:
                if unit.no_attack:
                    continue
                attack_options = [u for u in units if u.player !=
                                  unit.player and u.alive]
                if len(attack_options) == 0 or not unit.alive:
                    continue
                unit2 = random.choice(attack_options)
                u1_atk_str = unit.attack_strength + unit.tech['atk']
                u2_def_str = unit2.defense_strength + unit2.tech['def']
                hit_threshold = u1_atk_str - u2_def_str
                die_roll = random.randint(0, 6)
                if die_roll <= hit_threshold or die_roll == 1:
                    unit2.hurt()
                    self.log(unit2.name + " has been hurt by " + unit.name)

    # Run for 100 turns or until all of a player's units are dead
    def run_until_completion(self, max_turns=100):
        for _ in range(self.current_turn, max_turns):
            self.current_turn += 1
            self.complete_movement_phase()
            self.complete_combat_phase()
            self.complete_economic_phase()
            if self.rendering:
                self.grid.render()
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

    # Move all units from all players
    def complete_movement_phase(self):
        for player in self.players:
            self.log(player)
            for unit in player.units:
                if not unit.immovable:
                    unit.move(random.choice(unit.get_possible_spots()))
        self.grid.create()

    # Resolve combat between all units
    def complete_combat_phase(self):
        for _, units in self.grid.items():
            if not Grid.units_on_same_team(units):
                self.unit_battle(units)

    # Upgrade technology and buy new ships
    def complete_economic_phase(self):
        for player in self.players:
            income_list = [
                unit.cp_capacity for unit in player.units if type(unit) == Colony]
            player.pay(sum(income_list))
            player.pay_maitenance_costs()
            player.upgrade_tech()
            player.build_fleet()

    # Print to console if logging is enabled
    def log(self, *args):
        if self.logging:
            print(*args)

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

    # Prints all the players
    def __str__(self):
        string = "Game State: \n"
        for p in self.players:
            string += str(p) + "\n"
        return string
