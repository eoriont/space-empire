import random
from player.player import Player
from unit.colony import Colony
from board import Board
from unit.decoy import Decoy
from combat_engine import CombatEngine


class Game:
    # Initialize with 2 players and turn starts at 0
    def __init__(self, board_size, logging=False, rendering=False, die_mode="normal"):
        self.die_mode = die_mode
        self.current_id = 0
        self.last_die = 0
        self.current_turn = 0
        self.logging = logging
        self.rendering = rendering
        self.players = []
        self.player_count = 0
        self.board = Board(self, board_size)
        self.board.init_planets((3, 6), (3, 0))
        self.board.create()
        self.combat = CombatEngine(self)

    # Add player to the game before running
    def add_player(self, player):
        self.players.append(player)
        self.player_count = len(self.players)
        self.board.create()

    # Run for 100 turns or until all of a player's units are dead
    def run_until_completion(self, max_turns=100):
        for _ in range(self.current_turn, max_turns):
            self.current_turn += 1
            self.complete_movement_phase()
            self.complete_combat_phase()
            self.complete_economic_phase()
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

    # Move all units from  all players for phase
    def complete_singular_movement(self, phase):
        for player in self.players:
            self.log(f"{player.name} - Move {phase+1}")
            player.move_units(phase)
            self.log('')

    # Move all units from all players in 3 phases
    def complete_movement_phase(self):
        self.log(f"Turn {self.current_turn} - Movement Phase\n")
        for phase in range(3):
            self.complete_singular_movement(phase)
        self.render()
        self.log(self)
        self.log("------------------------")
        self.board.create()

    # Resolve combat between all units
    def complete_combat_phase(self):
        self.log(f"Turn {self.current_turn} - Combat Phase\n")
        for _, units in self.board.items():
            if not CombatEngine.units_on_same_team(units):
                self.combat.battle(units)
        self.log("------------------------")
        self.board.create()
        self.log(self)
        self.render()

    # Upgrade technology and buy new ships
    def complete_economic_phase(self):
        self.log(f"Turn {self.current_turn} - Economic Phase\n")
        for player in self.players:
            player.get_income()
            player.unit_economics()
            player.pay_maintenance_costs()
            player.upgrade_tech()
            player.build_fleet()
        self.log("------------------------")
        self.board.create()

    # Print to console if logging is enabled
    def log(self, *args):
        if self.logging:
            print(*args)

    # Render if rendering is enabled
    def render(self):
        if self.rendering:
            self.board.render()

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

    def die_roll(self):
        if self.die_mode == "ascend":
            self.last_die += 1
            return ((self.last_die-1) % 6) + 1
        elif self.die_mode == "normal":
            return random.randint(1, 6)
        elif self.die_mode == "descend":
            self.last_die -= 1
            return (self.last_die % 6) + 1

    def next_id():
        self.current_id += 1
        return self.current_id

    # Prints all the players
    def __str__(self):
        string = "Game State: \n"
        for p in self.players:
            string += str(p) + "\n"
        return string
