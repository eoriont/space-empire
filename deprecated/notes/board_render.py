# This goes in the board class, but is dead right now
# Make a graph of the game
def render(self):
    _, ax = plt.subplots()
    ax.xaxis.set_minor_locator(MultipleLocator(.5))
    ax.yaxis.set_minor_locator(MultipleLocator(.5))

    plt.title(''.join(
        [f"| {player.name}: {player.cp}CP |" for player in self.game.players]))

    for planet in self.planets:
        plt.gca().add_patch(plt.Circle(planet.pos, radius=.5, fc='g'))

    for pos, units in self.items():
        x, y = pos
        for i, unit in enumerate(units):
            offset = i/len(units)
            ax.text(x, y+offset, unit.id, fontsize=12, color=unit.player.color,
                    horizontalalignment='center', verticalalignment='center')

    x_max, y_max = self.size
    plt.xlim(-0.5, x_max-0.5)
    plt.ylim(-0.5, y_max-0.5)

    plt.grid(which='minor')
    plt.show()
