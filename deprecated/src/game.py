import random
import math
from player import Player
from board import Board
from combat_engine import CombatEngine
from movement_engine import MovementEngine
from economic_engine import EconomicEngine
from unit import Destroyer, Scout, Decoy, Colony, ColonyShip, ShipYard
from technology import Technology
import sys
sys.path.append("tests")
from otest import cstring


class Game:
    # Initialize with 2 players and turn starts at 0
    def __init__(self, board_size, logging=False, rendering=False, die_mode="normal", game_level=1, die_size=6, debug_mode=True):
        self.debug_mode = debug_mode
        self.die_size = die_size
        self.game_level = game_level
        self.die_mode = die_mode
        self.current_id = 0
        self.last_die = 0
        self.current_turn = 0
        self.logging = logging
        self.rendering = rendering
        self.players = []
        self.board = Board(self, board_size)
        self.board.init_planets((3, 6), (3, 0))
        self.board.create()
        self.combat = CombatEngine(self)
        self.movement = MovementEngine(self)
        self.economy = EconomicEngine(self)
        self.phase = "Beginning"
        self.round = 0
        self.winner = None
        self.current_player_id = 0

    # Add player to the game before running
    def add_player(self, player):
        self.players.append(player)
        player.id = len(self.players)-1

    def start(self):
        for player in self.players:
            player.start()
            self.log(f"{player.get_name()} uses {type(player.strat).__name__}")
        self.board.create()

    # Run for 100 turns or until all of a player's units are dead
    def run_until_completion(self, max_turns=100):
        if self.game_level == 2:
            self.phase = "Economic"
            self.economy.economic_phase(self.current_turn)
        while self.current_turn <= max_turns:
            self.current_turn += 1
            self.phase = "Movement"
            self.movement.movement_phase(self.current_turn)
            self.phase = "Combat"

            # Combat phase returns if someone won
            if self.combat.combat_phase(self.current_turn):
                break
            if self.game_level > 2:
                self.phase = "Economic"
                self.economy.economic_phase(self.current_turn)
            if self.test_for_winner():
                break
        self.winner = self.test_for_winner()
        if self.winner:
            self.log("We have a winner!!")
            self.log(f"Turns taken: {self.current_turn}")
            return True
        else:
            self.log("Nobody won!")
            return False

    def test_for_winner(self):
        alive_players = [(p, any(True for c in p.get_units() if type(c) == Colony and c.is_home_colony)) for p in self.players]

        loser = next((x[0] for x in alive_players if not x[1]), None)
        if loser is not None:
            alive_players.remove((loser, False))
            return alive_players[0][0]
        return None

    # Print to console if logging is enabled
    def log(self, *s):
        if self.logging:
            print(cstring(f"&6{self.current_turn} &4{self.phase} &3{', '.join(str(x) for x in s)}"))

    # Raise a prettier exception
    def throw(self, error, *details):
        if self.debug_mode:
            print(cstring(f"""
&1ERROR THROWN:
&7{error}
&1DETAILS:
&6Turn {self.current_turn} &4Phase {self.phase}
&7{', '.join(str(x) for x in details)}
                """
            ))
            import sys
            sys.exit(0)

    # # Render if rendering is enabled
    # def render(self):
    #     if self.rendering:
    #         self.board.render()

    def die_roll(self):
        if self.die_mode == "ascend":
            self.last_die += 1
            return ((self.last_die-1) % self.die_size) + 1
        elif self.die_mode == "normal":
            # return random.randint(1, self.die_size)
            #! This is a problem if we don't agree on exactly what this should be
            return math.ceil(self.die_size*random.random())
        elif self.die_mode == "descend":
            self.last_die -= 1
            return (self.last_die % self.die_size) + 1

    # Theoretically this should just be a nonrepeating value
    def next_id(self):
        self.current_id += 1
        return self.current_id

    def get_unit_data(self):
        return {
            "Scout": {"cp_cost": Scout.cp_cost, "shipsize_needed": Scout.req_size_tech, "hullsize": Scout.hull_size},
            "Destroyer": {"cp_cost": Destroyer.cp_cost, "shipsize_needed": Destroyer.req_size_tech, "hullsize": Destroyer.hull_size}
        }

    def unit_str_to_class(self, unit):
        return {
            "Scout": Scout,
            "Destroyer": Destroyer,
            "ColonyShip": ColonyShip,
            "ShipYard": ShipYard,
            "Colony": Colony
        }[unit]

    def generate_state(self, player=None, combat=False):
        return {
            'turn': self.current_turn,
            'winner': None,
            'players': [p.generate_state(player==p, combat) for p in self.players],
            'player_whose_turn': self.current_player_id,
            'phase': self.phase,
            'round': self.round,
            'technology_data': Technology.get_state(),
            'unit_data': self.get_unit_data(),
            'board_size': self.board.size
        }
