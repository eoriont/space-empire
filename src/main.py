from game import Game
from player.random_player import RandomPlayer
from player.dumb_player import DumbPlayer
from player.combat_player import CombatPlayer
game = Game((7, 7), logging=True, rendering=False)
# game.add_player(RandomPlayer("RandomPlayer", (3, 6), game, "red"))
# game.add_player(DumbPlayer("DumbPlayer", (3, 0), game, "blue"))
# game.add_player(DumbPlayer("DumbPlayer1", (3, 0), game, "red"))
# game.add_player(DumbPlayer("DumbPlayer2", (3, 6), game, "blue"))
game.add_player(CombatPlayer("CombatPlayer1", (3, 0), game, "red"))
game.add_player(CombatPlayer("CombatPlayer2", (3, 6), game, "blue"))
print(game)
game.run_until_completion(100)
game.board.render()
