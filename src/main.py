from game import Game
from strategies.aggressive_strategy import AggressiveStrategy
from player import Player
game = Game((5, 5), logging=True, rendering=False, die_mode="ascend")
p1 = Player(AggressiveStrategy(0), "AggressivePlayer1", (2, 0), game)
p2 = Player(AggressiveStrategy(1), "AggressivePlayer2", (2, 4), game)
game.add_player(p1)
game.add_player(p2)
game.start()
game.run_until_completion(10)
# game.board.render()
