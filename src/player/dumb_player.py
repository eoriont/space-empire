from player.player import Player
from unit.scout import Scout


class DumbPlayer(Player):
    # Only build scouts
    def build_fleet(self):
        while self.cp >= Scout.cp_cost:
            self.build_unit(Scout)

    # Never upgrade any technology
    def upgrade_tech(self):
        pass

    def move_units(self, phase):
        for unit in self.units:
            if type(unit) == Scout:
                pos = unit.pos_from_translation((1, 0))
                moves = self.tech.get_spaces()[phase]
                if pos in self.game.board.get_possible_spots(pos, moves):
                    unit.move(pos)
