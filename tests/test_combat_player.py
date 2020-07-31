import sys
sys.path.append('src')
try:
    from game import Game
    from unit.scout import Scout
    from unit.colony_ship import Colonyship
    from player.combat_player import CombatPlayer
    from otest import do_assert, assert_err, assert_success
except ImportError as e:
    print(e)

game = Game((5, 5), logging=False, rendering=False, perfect_die=True)


def assert_unit_positions(turn, phase, player, pos, units):
    board_units = [type(unit)
                   for unit in game.board[pos] if unit.player == player]
    unit_counts = {unit_type: board_units.count(
        unit_type) for unit_type in board_units}
    do_assert(f"unit positions turn {turn} phase {phase}", unit_counts, units)


p1 = CombatPlayer("CombatPlayer1", (2, 0), game, "red")
p2 = CombatPlayer("CombatPlayer2", (2, 4), game, "blue")
game.add_player(p1)
game.add_player(p2)

# Turn 1 Movement Phases
print("Movement Phase")
game.complete_singular_movement(0)
game.board.create()
assert_unit_positions(1, 1, p1, (2, 1), {Scout: 3, Colonyship: 3})
assert_unit_positions(1, 1, p2, (2, 3), {Scout: 3, Colonyship: 3})

game.complete_singular_movement(1)
game.board.create()
assert_unit_positions(1, 2, p1, (2, 2), {Scout: 3, Colonyship: 3})
assert_unit_positions(1, 2, p2, (2, 2), {Scout: 3, Colonyship: 3})

game.complete_singular_movement(2)
game.board.create()
assert_unit_positions(1, 3, p1, (2, 2), {Scout: 3, Colonyship: 3})
assert_unit_positions(1, 3, p2, (2, 2), {Scout: 3, Colonyship: 3})

# Turn 1 Combat Phase
print("Combat Phase")
game.complete_combat_phase()
game.board.create()
assert_unit_positions(1, 1, p1, (2, 2), {Scout: 3})
assert_unit_positions(1, 1, p2, (2, 2), {})

print("All tests passed!")
