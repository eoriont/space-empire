import sys
import random

sys.path.append('src')
sys.path.append('tests')
sys.path.append('src/strategies/lesson_strategies/level_3')
from game import Game

from attack_berserker_level_3 import AttackBerserkerLevel3
from numbers_berserker_level_3 import NumbersBerserkerLevel3

from player import Player
from otest import cstring

print("Playing games...")

def matchup(type1, type2):
    wins = [0, 0, 0]
    games = 20
    for i in range(games):
        first_player = 0 if i < 10 else 1
        random.seed(i+1)
        log = i in []
        game = Game((7, 7), logging=log, rendering=False, game_level=3, die_size=10)
        p1 = Player(type1(first_player), "Player1", (3, 0), game)
        p2 = Player(type2(1-first_player), "Player2", (3, 6), game)
        if first_player == 0:
            game.add_player(p1)
            game.add_player(p2)
        else:
            game.add_player(p2)
            game.add_player(p1)

        game.start()

        if game.run_until_completion(max_turns=100):
            print(type(game.winner.strat).__name__, i)
            wins[[type1, type2].index(type(game.winner.strat))] += 1
        else:
            print("tie", i)
            wins[2] += 1

        if log:
            input()
    wins = [w/games for w in wins]
    return wins

print(cstring("\n &5Numbers vs Attack Strategy"))
print(matchup(NumbersBerserkerLevel3, AttackBerserkerLevel3))
