import sys
sys.path.append('src')
try:
    from game import Game
    from unit.scout import Scout
    from strategies.dumb_strategy import DumbStrategy
    from player.player import Player
    from otest import do_assert, assert_bool, color_print
except ImportError as e:
    print(e)

game = Game((5, 5), logging=False, rendering=False, die_mode="ascend")


def assert_player_scouts(turn, player, pos, amt):
    p_units = game.board[pos]
    unit_types = [type(u) for u in p_units]
    is_player = all(u.player == player for u in p_units)
    amt_correct = unit_types.count(Scout) == amt
    assert_bool(f"turn {turn} movement phase", is_player and amt_correct)


def assert_player_economic(turn, player, cps):
    do_assert(f"turn {turn} economic phase", player.cp, cps)


p1 = Player(DumbStrategy(), "DumbPlayer1", (2, 0), game)
p2 = Player(DumbStrategy(), "DumbPlayer2", (2, 4), game)
game.add_player(p1)
game.add_player(p2)
game.start()

# 1 Movement Phase
print("Turn 1 Movement Phase")
game.movement.movement_phase(game.current_turn)
assert_player_scouts(1, p1, (4, 0), 3)
assert_player_scouts(1, p2, (4, 4), 3)

# 1 Combat Phase (nothing happens)
print("Turn 1 Combat Phase")
game.combat.combat_phase(game.current_turn)


# 1 Economic Phase
print("Turn 1 Economic Phase")
game.economy.economic_phase(game.current_turn)
assert_player_economic(1, p1, 5)
assert_player_economic(1, p2, 5)

assert_player_scouts(1, p1, (4, 0), 3)
assert_player_scouts(1, p2, (4, 4), 3)
assert_player_scouts(1, p1, (2, 0), 2)
assert_player_scouts(1, p2, (2, 4), 2)

# 2 Movement Phase
print("Turn 2 Movement Phase")
game.movement.movement_phase(game.current_turn)
assert_player_scouts(2, p1, (4, 0), 5)
assert_player_scouts(2, p2, (4, 4), 5)

# 2 Combat Phase (nothing happens)
print("Turn 2 Combat Phase")
game.combat.combat_phase(game.current_turn)

# 2 Economic Phase
print("Turn 2 Economic Phase")
game.economy.economic_phase(game.current_turn)
assert_player_economic(2, p1, 2)
assert_player_economic(2, p2, 2)

assert_player_scouts(2, p1, (4, 0), 5)
assert_player_scouts(2, p2, (4, 4), 5)
assert_player_scouts(2, p1, (2, 0), 3)
assert_player_scouts(2, p2, (2, 4), 3)

# 3 Movement Phase
print("Turn 3 Movement Phase")
game.movement.movement_phase(game.current_turn)
assert_player_scouts(3, p1, (4, 0), 8)
assert_player_scouts(3, p2, (4, 4), 8)

# 3 Combat Phase (nothing happens)
print("Turn 3 Combat Phase")
game.combat.combat_phase(game.current_turn)

# 3 Economic Phase
print("Turn 3 Economic Phase")
game.economy.economic_phase(game.current_turn)
assert_player_scouts(3, p1, (4, 0), 8)
assert_player_scouts(3, p2, (4, 4), 8)
assert_player_scouts(3, p1, (2, 0), 2)
assert_player_scouts(3, p2, (2, 4), 2)

assert_player_economic(3, p1, 2)
assert_player_economic(3, p2, 2)

# 4 Movement Phase
print("Turn 4 Movement Phase")
game.movement.movement_phase(game.current_turn)
assert_player_scouts(4, p1, (4, 0), 10)
assert_player_scouts(4, p2, (4, 4), 10)

# 4 Combat Phase (nothing happens)
print("Turn 4 Combat Phase")
game.combat.combat_phase(game.current_turn)

# 4 Economic Phase
print("Turn 4 Economic Phase")
game.economy.economic_phase(game.current_turn)
assert_player_scouts(4, p1, (4, 0), 10)
assert_player_scouts(4, p2, (4, 4), 10)

assert_player_economic(4, p1, 0)
assert_player_economic(4, p2, 0)

color_print("All tests passed!", "Blue")
