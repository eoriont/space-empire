from game import Game
# from strategies.aggressive_strategy import AggressiveStrategy
# from strategies.lesson_strategies.ripple_strategy_level_1 import RippleStrategyLevel1
from strategies.lesson_strategies.flanker_strategy_level_1 import FlankerStrategyLevel1
from player import Player
game = Game((5, 5), logging=True, rendering=False, game_level=1, die_size=10)
p1 = Player(FlankerStrategyLevel1(0), "Player0", (2, 0), game)
p2 = Player(FlankerStrategyLevel1(1), "Player1", (2, 4), game)
game.add_player(p1)
game.add_player(p2)
game.start()
game.run_until_completion(10)
# game.board.render()
