import sys
sys.path.append('src')
try:
    from game import Game
    from unit import Scout

    from strategies.lesson_strategies.berserker_strategy_level_1 import BerserkerStrategyLevel1

    from player import Player
    from otest import do_assert, assert_bool, color_print, cstring
except ImportError as e:
    print(e)

game = Game((5, 5), logging=False, rendering=False, simple_mode=True)

def assert_player_scouts(player, pos, amt):
    state = game.generate_state(True)
    units = [u for u in state['players'][player]['units']
             if u['coords'] == pos and u['type'] == 'Scout']
    assert_bool(f"end of game units", len(units) == amt)

print("Playing game...")
p1 = Player(BerserkerStrategyLevel1(0), "BerserkerLvl1-1", (2, 0), game)
p2 = Player(BerserkerStrategyLevel1(1), "BerserkerLvl1-1", (2, 4), game)
game.add_player(p1)
game.add_player(p2)
game.start()

game.run_until_completion(max_turns=float('inf'))

# Sometimes this fails due to random dice rolls
do_assert("winner", game.winner.id, 0)

print("Testing end of game scout positions")
assert_player_scouts(0, (2, 4), 2)
assert_player_scouts(1, (2, 0), 0)

print(cstring("&4All tests passed for BerserkerLvl1 vs BerserkerLvl1!"))