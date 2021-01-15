from technology import Technology


class EconomicEngine:
    def __init__(self, game):
        self.game = game

    # Upgrade technology and buy new ships
    def economic_phase(self, current_turn):
        self.game.phase = "Economic"
        for player in self.game.players:
            player.pay(player.get_income())
            maintenance = player.get_maintenance()

            while player.cp-maintenance < 0:
                removal = player.strat.decide_removal(
                    self.game.generate_state())
                self.remove_unit(removal, player)
                maintenance = player.get_maintenance()
            player.pay(-player.get_maintenance())

            purchases = player.strat.decide_purchases(
                self.game.generate_state())
            self.verify_purchases(purchases, player.cp, player.tech)
            self.purchase(purchases, player)

        self.game.board.create()

    def remove_unit(self, u, player):
        player.get_unit_by_id(u["id"]).destroy("planned demolition")

    def verify_purchases(self, purchases, cp, tech):
        # Verify the purchases are within budget
        # And player has sufficient tech
        u = purchases["units"]
        units = {x: u.count(x) for x in set(u)}
        unit_data = self.game.get_unit_data()
        units_cost = sum(unit_data[u]["cp_cost"] *
                         amt for u, amt in units.items())
        t = purchases["tech"]
        tech = {x: t.count(x) for x in set(t)}
        tech_cost = sum(sum(Technology.get_price({t: tech[t]+i}, t) for i in range(levels))
                        for t, levels in tech.items())

        if cp < units_cost + tech_cost:
            raise Exception("Player bought too many units/tech!")

    def purchase(self, purchases, player):
        u = purchases["units"]
        units = {x: u.count(x) for x in set(u)}
        for unit, amt in units.items():
            for _ in range(amt):
                player.build_unit(self.game.unit_str_to_class(unit))

        tech = purchases["tech"]
        for t in tech:
            player.buy_tech(t)

    def generate_economic_state(self):
        return [{
            'maintenance_cost': p.get_maintenance(),
            'income': p.get_income()
        } for player in self.game.players]
