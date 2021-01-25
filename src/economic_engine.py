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
        tech_purchases = purchases["technology"]
        te = Technology(tech.tech.copy())
        tech_cost = sum(te.buy_tech(t) for t in tech_purchases)

        units_cost = 0
        unit_data = self.game.get_unit_data()
        for u in purchases['units']:
            unit_type = u['type']
            if te['shipsize'] >= unit_data[unit_type]['shipsize_needed']:
                units_cost += unit_data[unit_type]['cp_cost']
            else:
                raise Exception("Player bought unit without sufficient shipsize!")

        if cp < units_cost + tech_cost:
            raise Exception("Player bought too many units/tech!")

    def purchase(self, purchases, player):
        units = purchases["units"]
        for unit in units:
            player.build_unit(self.game.unit_str_to_class(unit['type']), starting_pos=unit['coords'])

        tech = purchases["technology"]
        for t in tech:
            player.buy_tech(t)

    def generate_economic_state(self):
        return [{
            'maintenance_cost': p.get_maintenance(),
            'income': p.get_income()
        } for player in self.game.players]
