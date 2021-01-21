from unit import Unit, Colony


class ColonyShip(Unit):
    # ColonyShip unit's stats
    cp_cost = 8
    attack_strength = 0
    defense_strength = 0
    abbr = "CS"
    armor = 1
    hull_size = 1
    req_size_tech = 1
    default_tech = {'movement': 1}
    no_maintenance = True
    no_attack = True
    #! Somehow make it not affected by technology
    #! This shouldn't matter right now bc tests don't need it

    def test_for_planet(self):
        if self.game.board.on_unoccupied_planet(self.pos):
            # ask player to settle
            if self.player.strat.will_colonize_planet(self):
                col = self.player.build_unit(Colony, self.pos)
                self.destroy("turning into a colony")
