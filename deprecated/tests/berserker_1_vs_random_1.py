import sys
sys.path.append('src')
try:
    from game import Game
    from unit import Scout

    from strategies.lesson_strategies.level_1.berserker_strategy_level_1 import BerserkerStrategyLevel1
    from strategies.lesson_strategies.level_1.random_strategy_level_1 import RandomStrategyLevel1

    from player import Player
    from otest import do_assert, assert_bool, color_print, cstring
except ImportError as e:
    print(e)


def assert_player_scouts(player, pos, amt):
    state = game.generate_state(True)
    units = [u for u in state['players'][player]['units']
             if u['coords'] == pos and u['type'] == 'Scout']
    assert_bool(f"end of game units", len(units) == amt)

print("Playing games...")

wins = [0, 0]

for _ in range(100):
    game = Game((5, 5), logging=False, rendering=False, game_level=1)
    p1 = Player(BerserkerStrategyLevel1(0), "BerserkerLvl1", (2, 0), game)
    p2 = Player(RandomStrategyLevel1(1), "RandomLvl1", (2, 4), game)
    game.add_player(p1)
    game.add_player(p2)
    game.start()

    if game.run_until_completion(max_turns=100):
        wins[game.winner.id] += 1

do_assert("berserker is better than random player", wins[0] > wins[1], True)

print(cstring("&4All tests passed for BerserkerLvl1 vs RandomLvl1!"))
