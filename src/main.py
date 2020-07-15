from game import Game
from player.random_player import RandomPlayer
from player.dumb_player import DumbPlayer
game = Game((7, 7), logging=True, rendering=False)
print(game)
game.add_player(RandomPlayer("RandomPlayer", (3, 6), game, "red"))
game.add_player(DumbPlayer("DumbPlayer", (3, 0), game, "blue"))
game.run_until_completion()
game.board.render()
