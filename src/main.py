from game import Game
game = Game((7, 7), logging=True, rendering=False)
print(game)
game.run_until_completion()
game.board.render()
