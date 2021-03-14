import sys
import random
sys.path.append('src')
try:
    from game import Game
    from unit import Scout

    from strategies.lesson_strategies.level_1.berserker_strategy_level_1 import BerserkerStrategyLevel1
    from strategies.lesson_strategies.level_1.random_strategy_level_1 import RandomStrategyLevel1
    from strategies.lesson_strategies.level_1.dumb_strategy_level_1 import DumbStrategyLevel1
    from strategies.lesson_strategies.level_1.flanker_strategy_level_1 import FlankerStrategyLevel1
    from strategies.lesson_strategies.level_1.ripple_strategy_level_1 import RippleStrategyLevel1

    from player import Player
    from otest import do_assert, assert_bool, color_print, cstring
except ImportError as e:
    print(e)

print("Playing games...")

def matchup(type1, type2):
    wins = [0, 0]
    games = 1000
    for _ in range(games):
        game = Game((5, 5), logging=False, rendering=False, game_level=1, die_size=10)
        first_player = random.choice([0, 1])
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
            print("Tie!")
    wins = [w/games for w in wins]
    return wins

print(cstring("\n &5Berserker vs Dumb Strategy wins"))
print(matchup(BerserkerStrategyLevel1, DumbStrategyLevel1))

print(cstring("\n &5Berserker vs Random Strategy wins"))
print(matchup(BerserkerStrategyLevel1, RandomStrategyLevel1))

print(cstring("\n &5Flanker vs Random Strategy wins"))
print(matchup(FlankerStrategyLevel1, RandomStrategyLevel1))

print(cstring("\n &5Flanker vs Berserker Strategy wins"))
print(matchup(FlankerStrategyLevel1, BerserkerStrategyLevel1))

print(cstring("\n &5Ripple vs Berserker Strategy wins"))
print(matchup(RippleStrategyLevel1, BerserkerStrategyLevel1))

print(cstring("&4All matchups passed!"))
