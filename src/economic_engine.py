class EconomicEngine:
    def __init__(self, game):
        self.game = game

    # Upgrade technology and buy new ships
    def economic_phase(self, current_turn):
        for player in self.game.players:
            player.get_income()
            player.unit_economics()
            maintenance = player.get_maintenance()

            # Pass player_data in, should be immutable
            removals = player.strat.decide_removals(player_data)
            self.verify_removals(removals, player, maintenance)
            self.remove_units(removals)
            player.pay(-player.get_maintenance())

            purchases = player.strat.decide_purchases(options, cp)
            self.verify_purchases(purchases)
            self.purchase(purchases)

        self.game.board.create()

    def verify_removals(self, removals, player, maintenance):
        # Verify the maintenance price of removals
        # allows the player to pay maintenance
        removal_savings = sum(r.maintenance_cost for r in removals)
        if maintenance-removal_savings > player.cp:
            raise Error("Player must remove more ships!")

    def remove_units(self, removals, player):
        for u in removals:
            u.destroy("planned demolition")

    def verify_purchases(self, purchases, cp):
        # Verify the purchases are within budget
        # And player has sufficient tech
        units = purchases["units"]
        units_cost = sum(s.maintenance_cost for s in ships)
        tech = purchases["tech"]
        tech_cost = sum(t.get_price() for t in tech)

        if player.cp < units_cost + tech_cost:
            raise Error("Player bought too many units/tech!")

    def purchase(self, purchases, player):
        units = purchases["units"]
        for unit in units:
            # > Possible cheating if unit["pay"] is true
            player.build_unit(**unit)

        tech = purchases["tech"]
        for t in tech:
            player.buy_tech(t.type)
