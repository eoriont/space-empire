from Game import Game
game = Game((7, 7), logging=True, rendering=True)
print(game)
game.run_until_completion()
