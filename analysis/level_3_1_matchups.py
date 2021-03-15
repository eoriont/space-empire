import sys, random

sys.path.append('src')
sys.path.append('src/strategies/level_3_1')

from game import Game

from berserker_strategy import BerserkerStrategy
from stationary_strategy import StationaryStrategy

random.seed(5)

game = Game((7, 7), stdout="logs/3_1.txt", game_level=3)
game.start([BerserkerStrategy, StationaryStrategy])
game.run_until_completion(max_turns=5)
