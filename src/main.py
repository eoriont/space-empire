from game import Game
from strategies.combat_strategy import CombatStrategy
from player.player import Player
game = Game((5, 5), logging=False, rendering=False, die_mode="ascend")
p1 = Player(CombatStrategy(), "CombatPlayer1", (2, 0), game)
p2 = Player(CombatStrategy(), "CombatPlayer2", (2, 4), game)
game.add_player(p1)
game.add_player(p2)
game.start()
game.run_until_completion(100)
# game.board.render()
