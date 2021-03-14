import sys
import random

sys.path.append('src')
sys.path.append('tests')
sys.path.append('src/strategies/lesson_strategies/level_3')

from game import Game
from player import Player
from otest import cstring

from colby_strategy import ColbySiegeStrategyLevel3 as ColbyStrategyLevel3
from david_strategy import DavidStrategyLevel3
from elijah_strategy import ElijahStrategyLevel3
from george_strategy import GeorgeStrategyLevel3
from numbers_berserker import NumbersBerserkerLevel3
from riley_strategy import RileyStrategyLevel3


print("Playing games...")

def matchup(type1, type2):
    print(cstring(f"\n &5 {type1.__name__} vs {type2.__name__}"))
    wins = [0, 0, 0]
    games = 100
    winlog = False
    for i in range(games):
        first_player = 0 if i < games//2 else 1
        random.seed(i+1)
        log = i in []
        # log = True
        game = Game((7, 7), logging=log, rendering=False, game_level=3, die_size=10)
        p1 = Player(type1(first_player), "Player1", (3, 6*first_player), game)
        p2 = Player(type2(1-first_player), "Player2", (3, 6 - 6*first_player), game)
        if first_player == 0:
            game.add_player(p1)
            game.add_player(p2)
        else:
            game.add_player(p2)
            game.add_player(p1)

        game.start()

        if game.run_until_completion(max_turns=100):
            if winlog: print(type(game.winner.strat).__name__, i)
            wins[[type1, type2].index(type(game.winner.strat))] += 1
        else:
            if winlog: print("tie", i)
            wins[2] += 1

        if log:
            input()
    wins = [w/games for w in wins]
    return wins

# I had to change colby's strategy
# print(matchup(ColbyStrategyLevel3, GeorgeStrategyLevel3))
# print(matchup(ColbyStrategyLevel3, RileyStrategyLevel3))
# print(matchup(ColbyStrategyLevel3, ElijahStrategyLevel3))
# print(matchup(ColbyStrategyLevel3, DavidStrategyLevel3))

print(matchup(GeorgeStrategyLevel3, RileyStrategyLevel3))
print(matchup(GeorgeStrategyLevel3, ElijahStrategyLevel3))
print(matchup(GeorgeStrategyLevel3, DavidStrategyLevel3))

# print(matchup(RileyStrategyLevel3, ElijahStrategyLevel3))
# print(matchup(RileyStrategyLevel3, DavidStrategyLevel3))

# print(matchup(DavidStrategyLevel3, ElijahStrategyLevel3))

# print(matchup(NumbersBerserkerLevel3, ColbyStrategyLevel3))
print(matchup(NumbersBerserkerLevel3, GeorgeStrategyLevel3))
# print(matchup(NumbersBerserkerLevel3, RileyStrategyLevel3))
# print(matchup(NumbersBerserkerLevel3, ElijahStrategyLevel3))
# print(matchup(NumbersBerserkerLevel3, DavidStrategyLevel3))
