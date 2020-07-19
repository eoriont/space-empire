import sys
sys.path.append('src')
try:
    from game import Game
    from unit.scout import Scout
    from player.dumb_player import DumbPlayer
except ImportError as e:
    print(e)

game = Game((5, 5), logging=False, rendering=False)


def do_assert(test_name, output, expected):
    assert output == expected, f"Test {test_name} failed: {output} was expected to be {expected}"
    print(f"Test {test_name} has PASSED!")


def assert_player_scouts(turn, player, pos, amt):
    p_units = game.board[pos]
    unit_types = [type(u) for u in p_units]
    is_player = all(u.player == player for u in p_units)
    amt_correct = unit_types.count(Scout) == amt
    assert is_player and amt_correct, f"Test turn {turn} movement phase failed! Units at pos {pos}: {p_units}"
    print(f"Test turn {turn} movement phase passed!")


def assert_player_economic(turn, player, cps):
    assert player.construction_points == cps, f"Test turn {turn} economic phase failed: player cp is {player.construction_points} but was expected to be {cps}"
    print(f"Test turn {turn} economic phase passed!")


p1 = DumbPlayer("DumbPlayer1", (2, 0), game, "red")
p2 = DumbPlayer("DumbPlayer2", (2, 4), game, "blue")
game.add_player(p1)
game.add_player(p2)

# 1 Movement Phase
game.complete_movement_phase()
assert_player_scouts(1, p1, (4, 0), 3)
assert_player_scouts(1, p2, (4, 4), 3)

# 1 Combat Phase (nothing happens)
game.complete_combat_phase()


# 1 Economic Phase
game.complete_economic_phase()
assert_player_economic(1, p1, 2)
assert_player_economic(1, p2, 2)

assert_player_scouts(1, p1, (4, 0), 3)
assert_player_scouts(1, p2, (4, 4), 3)
assert_player_scouts(1, p1, (2, 0), 3)
assert_player_scouts(1, p2, (2, 4), 3)

# 2 Movement Phase
game.complete_movement_phase()
assert_player_scouts(2, p1, (4, 0), 6)
assert_player_scouts(2, p2, (4, 4), 6)

# 2 Combat Phase (nothing happens)
game.complete_combat_phase()

# 2 Economic Phase
game.complete_economic_phase()
assert_player_economic(2, p1, 0)
assert_player_economic(2, p2, 0)

assert_player_scouts(2, p1, (4, 0), 5)
assert_player_scouts(2, p2, (4, 4), 5)

# 3 Movement Phase
game.complete_movement_phase()
assert_player_scouts(3, p1, (4, 0), 5)
assert_player_scouts(3, p2, (4, 4), 5)

# 3 Combat Phase (nothing happens)
game.complete_combat_phase()

# 3 Economic Phase
game.complete_economic_phase()
assert_player_scouts(3, p1, (4, 0), 3)
assert_player_scouts(3, p2, (4, 4), 3)

assert_player_economic(3, p1, 0)
assert_player_economic(3, p2, 0)

# 4 Movement Phase
game.complete_movement_phase()
assert_player_scouts(4, p1, (4, 0), 3)
assert_player_scouts(4, p2, (4, 4), 3)

# 4 Combat Phase (nothing happens)
game.complete_combat_phase()

# 4 Economic Phase
game.complete_economic_phase()
assert_player_scouts(4, p1, (4, 0), 3)
assert_player_scouts(4, p2, (4, 4), 3)

assert_player_economic(4, p1, 0)
assert_player_economic(4, p2, 0)

print("All tests passed!")
