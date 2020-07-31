from game import Game
from player.random_player import RandomPlayer
from player.dumb_player import DumbPlayer
from player.combat_player import CombatPlayer
game = Game((5, 5), logging=True, rendering=False, perfect_die=True)
# game.add_player(RandomPlayer("RandomPlayer", (3, 6), game, "red"))
# game.add_player(DumbPlayer("DumbPlayer", (3, 0), game, "blue"))
# game.add_player(DumbPlayer("DumbPlayer1", (3, 0), game, "red"))
# game.add_player(DumbPlayer("DumbPlayer2", (3, 6), game, "blue"))
game.add_player(CombatPlayer("CombatPlayer1", (2, 0), game, "red"))
game.add_player(CombatPlayer("CombatPlayer2", (2, 4), game, "blue"))
print(game)
game.run_until_completion(1)
game.board.render()
