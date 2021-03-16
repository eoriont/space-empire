import sys, random
sys.path.append('src')
sys.path.append('src/strategies/level_3_1')

from game import Game

from berserker_strategy import BerserkerStrategy
from stationary_strategy import StationaryStrategy

for i in range(1, 6):
    random.seed(i)
    game = Game((7, 7), stdout=f"logs/3_{i}.txt", game_level=3)
    game.start([BerserkerStrategy, StationaryStrategy])
    game.run_until_completion(max_turns=5)
