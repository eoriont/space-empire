from technology import Technology


class EconomicEngine:
    def __init__(self, game):
        self.game = game

    # Upgrade technology and buy new ships
    def economic_phase(self, current_turn):
        self.game.phase = "Economic"
        self.game.log("")
        for player in self.game.players:
            player.pay(player.get_income())
            maintenance = player.get_maintenance()
            self.game.log(f"{player.get_name()} starts economic phase with &5{player.cp}cp&3, after getting &5{player.get_income()}cp&3 as income")

            while player.cp-maintenance < 0:
                state = self.game.generate_state()
                removal = player.strat.decide_removal(state)
                removal = player.units[state['players'][player.id]['units'][removal]['id']]
                removal.destroy("planned demolition")
                maintenance = player.get_maintenance()
            self.game.log(f"Their maintenance costs are &5{maintenance}cp")
            player.pay(-maintenance)
            purchases = player.strat.decide_purchases(
                self.game.generate_state(player=player))
            self.verify_purchases(purchases, player.cp, player.tech)
            self.purchase(purchases, player)
            self.game.log(f"{player.get_name()} ends economic phase with &5{player.cp}cp")


        self.game.board.create()

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
            unit_pos = u['coords']
            if self.game.game_level == 2 and unit_type != 'Scout':
                raise Exception("Can only buy Scouts in level 2 game!")
            if te['shipsize'] >= unit_data[unit_type]['shipsize_needed']:
                units_cost += unit_data[unit_type]['cp_cost']
            else:
                raise Exception("Player bought unit without sufficient shipsize!")

            # Check if unit is being built on a colony (if it's a shipyard)
            if u['type'] == "ShipYard":
                if not self.game.board.contains(unit_pos, "Colony"):
                    raise Exception("ShipYards can only be built at colonies!")
            else:
                # Otherwise check if it's being built on a shipyard
                if not self.game.board.contains(unit_pos, "ShipYard"):
                    raise Exception("Ships can only be built at shipyards!")

        if cp < units_cost + tech_cost:
            raise Exception("Player bought too many units/tech!")

    def purchase(self, purchases, player):
        tech = purchases["technology"]
        for t in tech:
            p = player.buy_tech(t)
            self.game.log(f"They bought &2{t}&3 for &5{p}cp")

        units = purchases["units"]
        for unit in units:
            u = player.build_unit(self.game.unit_str_to_class(unit['type']), starting_pos=unit['coords'])
            self.game.log(f"They bought &2{u.get_name()}&3 for &5{u.cp_cost}")

    def generate_economic_state(self):
        return [{
            'maintenance_cost': p.get_maintenance(),
            'income': p.get_income()
        } for player in self.game.players]
