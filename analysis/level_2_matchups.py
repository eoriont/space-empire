import sys
import random
sys.path.append('src')
sys.path.append('test')
from game import Game
from unit import Scout

from strategies.lesson_strategies.level_2.attack_berserker_level_2 import AttackBerserkerLevel2
from strategies.lesson_strategies.level_2.numbers_berserker_level_2 import NumbersBerserkerLevel2
from strategies.lesson_strategies.level_2.defense_berserker_level_2 import DefenseBerserkerLevel2
from strategies.lesson_strategies.level_2.flanker_level_2 import FlankerStrategyLevel2
from strategies.lesson_strategies.level_2.movement_berserker_level_2 import MovementBerserkerLevel2

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
            # print(type(game.winner.strat).__name__, i)
            wins[[type1, type2].index(type(game.winner.strat))] += 1
        else:
            # print("tie", i)
            wins[2] += 1
    wins = [w/games for w in wins]
    return wins

print(cstring("\n &5Numbers vs Movement Strategy"))
print(matchup(NumbersBerserkerLevel2, MovementBerserkerLevel2))

print(cstring("\n &5Numbers vs Attack Strategy"))
print(matchup(NumbersBerserkerLevel2, AttackBerserkerLevel2))

print(cstring("\n &5Numbers vs Defense Strategy"))
print(matchup(NumbersBerserkerLevel2, DefenseBerserkerLevel2))

print(cstring("\n &5Numbers vs Flanker Strategy"))
print(matchup(NumbersBerserkerLevel2, FlankerStrategyLevel2))

print(cstring("\n &5Movement vs Attack Strategy"))
print(matchup(MovementBerserkerLevel2, AttackBerserkerLevel2))

print(cstring("\n &5Movement vs Defense Strategy"))
print(matchup(MovementBerserkerLevel2, DefenseBerserkerLevel2))

print(cstring("\n &5Movement vs Flanker Strategy"))
print(matchup(MovementBerserkerLevel2, FlankerStrategyLevel2))

print(cstring("\n &5Attack vs Defense Strategy"))
print(matchup(AttackBerserkerLevel2, DefenseBerserkerLevel2))

print(cstring("\n &5Attack vs Flanker Strategy"))
print(matchup(AttackBerserkerLevel2, FlankerStrategyLevel2))

print(cstring("\n &5Defense vs Flanker Strategy"))
print(matchup(DefenseBerserkerLevel2, FlankerStrategyLevel2))

print(cstring("&4All matchups passed!"))
