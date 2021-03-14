import sys
import random
import math
sys.path.append('src')
sys.path.append('tests')
from game import Game
from unit import Scout

from strategies.lesson_strategies.level_1.berserker_strategy_level_1 import BerserkerStrategyLevel1
from strategies.lesson_strategies.level_1.flanker_strategy_level_1 import FlankerStrategyLevel1

from player import Player
from otest import do_assert, assert_bool, color_print, cstring

print("Playing games...")

def matchup(type1, type2):
    wins = [0, 0]
    games = 20
    for i in range(games):
        first_player = 0 if i < 10 else 1
        log = True
        random.seed(i+1)
        game = Game((5, 5), logging=log, rendering=False, game_level=1, die_size=10)
        p1 = Player(type1(first_player), "Player1", (2, 0), game)
        p2 = Player(type2(1-first_player), "Player2", (2, 4), game)
        if first_player == 0:
            game.add_player(p1)
            game.add_player(p2)
        else:
            game.add_player(p2)
            game.add_player(p1)

        game.start()

        if game.run_until_completion(max_turns=100):
            winner = [type1, type2].index(type(game.winner.strat))
            wins[winner] += 1
            print(f"{type(game.winner.strat).__name__} won game {i}!")
        else:
            print("Tie!")
        print("Next game...")
    wins = [w/games for w in wins]
    return wins

print(cstring("&5Flanker vs Berserker Strategy"))
print(matchup(FlankerStrategyLevel1, BerserkerStrategyLevel1))

# To run this and output into a file, just run:
# python analysis/seeded_berserker.py >logs/21-02-05-flanker-vs-berserker.txt
