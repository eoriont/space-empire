from combat_engine import CombatEngine
from economic_engine import EconomicEngine
from log import Log
from movement_engine import MovementEngine
from player import Player
import math, random

from win_exception import WinException

class Game:
    def __init__(self, board_size=(7, 7), stdout=False, die_mode="normal", game_level=3, die_size=10, debug_mode=True):
        self.state = {
            "players": {},
            "units": {},
            "board_size": board_size,
            "winner": None,
            "turn": 1,
            "board_state": {},
            "die_mode": die_mode,
            "game_level": game_level,
            "die_size": die_size,
            "current_id": 0,
            "log": Log(stdout, debug_mode),
            "last_die": 0,
            "die_roll": self.die_roll,
            "current_player": None
        }

    def start(self, strategies):
        # Create all players
        for i, strategy in enumerate(strategies):
            pos = (3, 0 if i == 0 else 6)
            Player.init(self.state, i+1, strategy, pos)

        # Make planets
        self.state["planets"] = [(3, 0), (3, 6)]

    # Run for 100 turns or until all of a player's units are dead
    def run_until_completion(self, max_turns=100):
        if self.state["game_level"] == 2:
            EconomicEngine.run_phase(self.state)
        while self.state["turn"] <= max_turns:
            MovementEngine.run_phase(self.state)

            try:
                # Combat Engine raises exception if someone wins
                CombatEngine.run_phase(self.state)
            except WinException:
                break

            if self.state["game_level"] > 2:
                EconomicEngine.run_phase(self.state)

            self.state["turn"] += 1

        self.state["log"].save()
        if self.state["winner"]:
            return True
        else:
            return False

    def die_roll(self):
        if self.state["die_mode"] == "ascend":
            self.state["last_die"] += 1
            return ((self.state["last_die"]-1) % self["die_size"]) + 1
        elif self.state["die_mode"]  == "normal":
            return math.ceil(self.state["die_size"]*random.random())
        elif self.state["die_mode"] == "descend":
            self.state["last_die"] -= 1
            return (self.state["last_die"] % self.state["die_size"]) + 1

    def get_winner(self):
        if self.state["winner"] != None:
            return type(Player.from_id(self.state["winner"])["strategy"])
