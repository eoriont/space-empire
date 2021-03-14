import sys
import random
sys.path.append('src')
sys.path.append('tests')
sys.path.append('src/strategies/lesson_strategies/level_2')
from game import Game

from colby_strategy import ColbyStrategyLevel2
from david_strategy import DavidStrategyLevel2
from elijah_strategy import ElijahStrategyLevel2
from george_strategy import GeorgeStrategyLevel2
from justin_strategy import JustinStrategyLevel2
from riley_strategy import RileyStrategyLevel2
from numbers_berserker_level_2 import NumbersBerserkerLevel2

from player import Player
from otest import cstring

print("Playing games...")

def matchup(type1, type2):
    wins = [0, 0, 0]
    games = 500
    for i in range(games):
        first_player = 0 if i < games/2 else 1
        random.seed(i+1)
        log = i in []
        game = Game((5, 5), logging=log, rendering=False, game_level=2, die_size=10)
        p1 = Player(type1(first_player), "Player1", (2, 0), game)
        p2 = Player(type2(1-first_player), "Player2", (2, 4), game)
        if first_player == 0:
            game.add_player(p1)
            game.add_player(p2)
        else:
            game.add_player(p2)
            game.add_player(p1)

        game.start()


        if game.run_until_completion(max_turns=50):
            wins[[type1, type2].index(type(game.winner.strat))] += 1
        else:
            wins[2] += 1
        if log:
            input()
    wins = [w/games for w in wins]
    return wins

print(cstring("\n &5 Colby vs George"))
print(matchup(ColbyStrategyLevel2, GeorgeStrategyLevel2))

print(cstring("\n &5 Colby vs Riley"))
print(matchup(ColbyStrategyLevel2, RileyStrategyLevel2))

# =================================================================
print(cstring("\n &5 Colby vs Elijah"))
print(matchup(ColbyStrategyLevel2, ElijahStrategyLevel2))
# =================================================================

print(cstring("\n &5 Colby vs David"))
print(matchup(ColbyStrategyLevel2, DavidStrategyLevel2))

print(cstring("\n &5 Colby vs Justin"))
print(matchup(ColbyStrategyLevel2, JustinStrategyLevel2))

print(cstring("\n &5 George vs Riley"))
print(matchup(GeorgeStrategyLevel2, RileyStrategyLevel2))

# =================================================================
print(cstring("\n &5 George vs Elijah"))
print(matchup(GeorgeStrategyLevel2, ElijahStrategyLevel2))
# =================================================================

print(cstring("\n &5 George vs David"))
print(matchup(GeorgeStrategyLevel2, DavidStrategyLevel2))

print(cstring("\n &5 George vs Justin"))
print(matchup(GeorgeStrategyLevel2, JustinStrategyLevel2))

# =================================================================
print(cstring("\n &5 Riley vs Elijah"))
print(matchup(RileyStrategyLevel2, ElijahStrategyLevel2))
# =================================================================

print(cstring("\n &5 Riley vs David"))
print(matchup(RileyStrategyLevel2, DavidStrategyLevel2))

print(cstring("\n &5 Riley vs Justin"))
print(matchup(RileyStrategyLevel2, JustinStrategyLevel2))

# =================================================================
print(cstring("\n &5 Elijah vs David"))
print(matchup(ElijahStrategyLevel2, DavidStrategyLevel2))

print(cstring("\n &5 Elijah vs Justin"))
print(matchup(ElijahStrategyLevel2, JustinStrategyLevel2))
# =================================================================

print(cstring("\n &5 David vs Justin"))
print(matchup(DavidStrategyLevel2, JustinStrategyLevel2))

print(cstring("\n &5 Numbers vs Colby"))
print(matchup(NumbersBerserkerLevel2, ColbyStrategyLevel2))

print(cstring("\n &5 Numbers vs George"))
print(matchup(NumbersBerserkerLevel2, GeorgeStrategyLevel2))

print(cstring("\n &5 Numbers vs Riley"))
print(matchup(NumbersBerserkerLevel2, RileyStrategyLevel2))

# =================================================================
print(cstring("\n &5 Numbers vs Elijah"))
print(matchup(NumbersBerserkerLevel2, ElijahStrategyLevel2))
# =================================================================

print(cstring("\n &5 Numbers vs David"))
print(matchup(NumbersBerserkerLevel2, DavidStrategyLevel2))

print(cstring("\n &5 Numbers vs Justin"))
print(matchup(NumbersBerserkerLevel2, JustinStrategyLevel2))


print(cstring("&4All matchups passed!"))
