import random
from player.player import Player
from unit.colony import Colony
from unit.colony_ship import Colonyship
from unit.ship_yard import ShipYard
from board import Board
from unit.decoy import Decoy
from combat_engine import CombatEngine
from movement_engine import MovementEngine
from economic_engine import EconomicEngine
from unit.scout import Scout
from unit.destroyer import Destroyer
from technology import Technology


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
        self.board = Board(self, board_size)
        self.board.init_planets((3, 6), (3, 0))
        self.board.create()
        self.combat = CombatEngine(self)
        self.movement = MovementEngine(self)
        self.economy = EconomicEngine(self)
        self.phase = ""
        self.round = 0
        self.winner = None
        self.current_player_id = 0

    # Add player to the game before running
    def add_player(self, player):
        self.players.append(player)
        player.id = len(self.players)
        self.board.create()

    def start(self):
        for player in self.players:
            player.start()

    # Run for 100 turns or until all of a player's units are dead
    def run_until_completion(self, max_turns=100):
        for _ in range(self.current_turn, max_turns):
            self.current_turn += 1
            self.phase = "Movement"
            self.movement.movement_phase(self.current_turn)
            self.phase = "Combat"
            self.combat.combat_phase(self.current_turn)
            self.phase = "Economic"
            self.economy.economic_phase(self.current_turn)
            if self.test_for_winner():
                break
        self.winner = self.test_for_winner()
        if self.winner:
            print("We have a winner!!")
            print("Turns taken:", self.current_turn)
        else:
            print("Nobody won!")

    def test_for_winner(self):
        ps = [len(p.units) for p in self.players]

        loser = bool(ps.count(0))
        if loser:
            del self.players[ps.index(0)]
            winner = self.players[0]
            return winner
        return False

    # Print to console if logging is enabled
    def log(self, *args):
        if self.logging:
            print(*args)

    # Render if rendering is enabled
    def render(self):
        if self.rendering:
            self.board.render()

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

    def get_unit_data(self):
        return {
            "Scout": {"cp_cost": Scout.cp_cost, "req_size_tech": Scout.req_size_tech},
            "Destroyer": {"cp_cost": Destroyer.cp_cost, "req_size_tech": Destroyer.req_size_tech}
        }

    def unit_str_to_class(self, unit):
        return {
            "Scout": Scout,
            "Destroyer": Destroyer,
            "Colonyship": Colonyship,
            "ShipYard": ShipYard,
            "Colony": Colony
        }[unit]

    def generate_state(self):

        players = [{
            'cp': p.cp,
            'id': i,
            #! spaces wasn't in the specification, figure out a way to remove it
            'spaces': p.tech.get_spaces(),
            'units': [{
                'id': j,
                'coords': u.pos,
                'type': type(u).__name__,
                'hits': type(u).armor-u.armor,
                'technology': u.tech.get_obj_state(),
                'player': i
            } for j, u in enumerate(p.units)],
            'tech': p.tech.tech.copy()
        } for i, p in enumerate(self.players)]

        return {
            'turn': self.current_turn,
            'winner': None,
            'players': players,
            'player_whose_turn': self.current_player_id,
            'planets': self.board.planets,
            'phase': self.phase,
            'round': self.round,
            'technology_data': Technology.get_state(),
            'unit_data': self.get_unit_data(),
            'board_size': self.board.size
        }
