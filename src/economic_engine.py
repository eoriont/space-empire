from technology import Technology


class EconomicEngine:
    def __init__(self, game):
        self.game = game

    # Upgrade technology and buy new ships
    def economic_phase(self, current_turn):
        for player in self.game.players:
            player.get_income()
            maintenance = player.get_maintenance()

            # Pass player_data in, should be immutable
            removals = player.strat.decide_removals(
                player.economic_state(), player.cp-maintenance)
            self.verify_removals(removals, player, maintenance)
            self.remove_units(removals, player)
            player.pay(-player.get_maintenance())

            options = self.game.get_unit_types()
            purchases = player.strat.decide_purchases(
                options, player.cp, player.tech.get_state(), player.economic_state())
            self.verify_purchases(purchases, player.cp)
            self.purchase(purchases, player)

        self.game.board.create()

    def verify_removals(self, removals, player, maintenance):
        # Verify the maintenance price of removals
        # allows the player to pay maintenance
        removal_savings = sum(r["maintenance_cost"] for r in removals)
        if maintenance-removal_savings > player.cp:
            raise Exception("Player must remove more ships!")

    def remove_units(self, removals, player):
        for u in removals:
            player.get_unit_by_id(u["id"]).destroy("planned demolition")

    def verify_purchases(self, purchases, cp):
        # Verify the purchases are within budget
        # And player has sufficient tech
        units = purchases["units"]
        unit_types = self.game.get_unit_types()
        units_cost = sum(unit_types[u]["cp_cost"] *
                         amt for u, amt in units.items())
        tech = purchases["tech"]
        tech_cost = sum(sum(Technology.get_price({t: i-1}, t) for i in levels)
                        for t, levels in tech.items())

        if cp < units_cost + tech_cost:
            raise Exception("Player bought too many units/tech!")

    def purchase(self, purchases, player):
        units = purchases["units"]
        for unit, amt in units.items():
            for _ in range(amt):
                player.build_unit(self.game.unit_str_to_class(unit))

        tech = purchases["tech"]
        for t in tech:
            player.buy_tech(t)
