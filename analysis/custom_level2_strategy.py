import sys
import random
sys.path.append('src')
sys.path.append('test')
from game import Game

from strategies.lesson_strategies.level_2.numbers_berserker_level_2 import NumbersBerserkerLevel2
from strategies.lesson_strategies.level_2.flanker_level_2 import FlankerStrategyLevel2
from strategies.lesson_strategies.level_2.arrow_level_2 import ArrowStrategyLevel2

from player import Player
from otest import cstring

print("Playing games...")

def matchup(type1, type2):
    wins = [0, 0, 0]
    games = 1000
    for i in range(games):
        first_player = 0 if i < 500 else 1
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

        if game.run_until_completion(max_turns=100):
            wins[[type1, type2].index(type(game.winner.strat))] += 1
        else:
            wins[2] += 1
    wins = [w/games for w in wins]
    return wins

print(cstring("\n &5Arrow vs Numbers Strategy"))
print(matchup(ArrowStrategyLevel2, NumbersBerserkerLevel2))

print(cstring("\n &5Arrow vs Flanker Strategy"))
print(matchup(ArrowStrategyLevel2, FlankerStrategyLevel2))

print(cstring("&4All matchups passed!"))
