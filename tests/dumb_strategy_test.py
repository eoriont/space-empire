import sys
sys.path.append('src')
try:
    from game import Game
    from unit import Scout

    # Change this line to use other people's strategies
    # from strategies.dumb_strategy import DumbStrategy
    # from strategies.imported.riley_dumb_strategy import DumbStrategy
    # from strategies.imported.colby_dumb_strategy import DumbStrategy
    # from strategies.imported.george_dumb_strategy import DumbStrategy
    from strategies.imported.david_dumb_strategy import DumbStrategy

    from player import Player
    from otest import do_assert, assert_bool, color_print
except ImportError as e:
    print(e)

game = Game((5, 5), logging=False, rendering=False, die_mode="ascend", game_level=10)

def assert_player_scouts(turn, player, pos, amt):
    state = game.generate_state()
    units = [u for u in state['players'][player]['units']
             if u['coords'] == pos and u['type'] == 'Scout']
    assert_bool(f"turn {turn} movement phase", len(units) == amt)


def assert_player_economic(turn, player, cps):
    state = game.generate_state()
    do_assert(f"turn {turn} economic phase",
              state['players'][player]['cp'], cps)


p1 = Player(DumbStrategy(0), "DumbPlayer1", (2, 0), game)
p2 = Player(DumbStrategy(1), "DumbPlayer2", (2, 4), game)
game.add_player(p1)
game.add_player(p2)
game.start()

# 1 Movement Phase
print("Turn 1 Movement Phase")
game.movement.movement_phase(game.current_turn)
assert_player_scouts(1, 0, (4, 0), 3)
assert_player_scouts(1, 1, (4, 4), 3)

# 1 Combat Phase (nothing happens)
print("Turn 1 Combat Phase")
game.combat.combat_phase(game.current_turn)


# 1 Economic Phase
print("Turn 1 Economic Phase")
game.economy.economic_phase(game.current_turn)
assert_player_economic(1, 0, 5)
assert_player_economic(1, 1, 5)
assert_player_scouts(1, 0, (4, 0), 3)
assert_player_scouts(1, 1, (4, 4), 3)
assert_player_scouts(1, 0, (2, 0), 2)
assert_player_scouts(1, 1, (2, 4), 2)

# 2 Movement Phase
print("Turn 2 Movement Phase")
game.movement.movement_phase(game.current_turn)
assert_player_scouts(2, 0, (4, 0), 5)
assert_player_scouts(2, 1, (4, 4), 5)

# 2 Combat Phase (nothing happens)
print("Turn 2 Combat Phase")
game.combat.combat_phase(game.current_turn)

# 2 Economic Phase
print("Turn 2 Economic Phase")
game.economy.economic_phase(game.current_turn)
assert_player_economic(2, 0, 2)
assert_player_economic(2, 1, 2)

assert_player_scouts(2, 0, (4, 0), 5)
assert_player_scouts(2, 1, (4, 4), 5)
assert_player_scouts(2, 0, (2, 0), 3)
assert_player_scouts(2, 1, (2, 4), 3)

# 3 Movement Phase
print("Turn 3 Movement Phase")
game.movement.movement_phase(game.current_turn)
assert_player_scouts(3, 0, (4, 0), 8)
assert_player_scouts(3, 1, (4, 4), 8)

# 3 Combat Phase (nothing happens)
print("Turn 3 Combat Phase")
game.combat.combat_phase(game.current_turn)

# 3 Economic Phase
print("Turn 3 Economic Phase")
game.economy.economic_phase(game.current_turn)
assert_player_scouts(3, 0, (4, 0), 8)
assert_player_scouts(3, 1, (4, 4), 8)
assert_player_scouts(3, 0, (2, 0), 2)
assert_player_scouts(3, 1, (2, 4), 2)

assert_player_economic(3, 0, 2)
assert_player_economic(3, 1, 2)

# 4 Movement Phase
print("Turn 4 Movement Phase")
game.movement.movement_phase(game.current_turn)
assert_player_scouts(4, 0, (4, 0), 10)
assert_player_scouts(4, 1, (4, 4), 10)

# 4 Combat Phase (nothing happens)
print("Turn 4 Combat Phase")
game.combat.combat_phase(game.current_turn)

# 4 Economic Phase
print("Turn 4 Economic Phase")
game.economy.economic_phase(game.current_turn)
assert_player_scouts(4, 0, (4, 0), 10)
assert_player_scouts(4, 1, (4, 4), 10)

assert_player_economic(4, 0, 0)
assert_player_economic(4, 1, 0)

color_print("All tests passed!", "Blue")
