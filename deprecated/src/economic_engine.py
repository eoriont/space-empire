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
            self.verify_and_make_purchases(purchases, player)
            self.game.log(f"{player.get_name()} ends economic phase with &5{player.cp}cp")


        self.game.board.create()

    def verify_and_make_purchases(self, purchases, player):
        tech = purchases["technology"]
        tech_data = Technology.get_state()
        for t in tech:
            cp = player.cp
            tech_cost = tech_data[t][player.tech[t]]
            if cp < tech_cost:
                self.game.throw(f"Can't afford unit!",
                    f"""
&4Player {player.id} tried to buy {t}
&4They had &3{cp} cp&4, which is less than the required &3{tech_cost} cp&4 to buy {t}
                    """
                )
            else:
                p = player.buy_tech(t)
                self.game.log(f"They bought &2{t}&3 for &5{p}cp")

        unit_data = self.game.get_unit_data()
        syc = {}
        for u in purchases['units']:
            cp = player.cp
            unit_type = u['type']
            unit_pos = u['coords']
            unit_class = self.game.unit_str_to_class(unit_type)
            if unit_pos not in syc:
                syc[unit_pos] = self.game.board.get_shipyard_capacity(unit_pos)
            if self.state["game_level"] in (2, 3) and unit_type != 'Scout':
                self.game.throw("Can only buy Scouts in level 2 game!",
                    f"""
&4Player {player.id} tried to buy {unit_type} at {unit_pos}
&1This is a level {self.state["game_level"]} game, so player can only buy Scouts!
&4They had &3{cp} cp
                    """
                )
            elif player.tech['shipsize'] < unit_data[unit_type]['shipsize_needed']:
                self.game.throw("Player bought unit without sufficient shipsize tech!",
                    f"""
&4Player {player.id} tried to buy {unit_type} at {unit_pos}
&4Their shipsize tech level is {player.tech['shipsize']}
&4They had &3{cp} cp
                    """
                )
            elif unit_type == "ShipYard" and not self.game.board.contains(unit_pos, "Colony"):
                # Check if unit is being built on a colony (if it's a shipyard)
                self.game.throw("ShipYards can only be built at colonies!",
                    f"""
&4Player {player.id} tried to buy {unit_type} at {unit_pos}
&4They could afford it
&1There is no detected colony at {unit_pos}.
Here are the player's units at that position:
{[x for x in self.game.board[unit_pos] if x.player.id == player.id]}
Here are the other player's units that position:
{[x for x in self.game.board[unit_pos] if x.player.id != player.id]}
&4They had &3{cp} cp
                    """
                )
            elif not self.game.board.contains(unit_pos, "ShipYard"):
                # Otherwise check if it's being built on a shipyard
                self.game.throw(f"{unit_type} can only be built at ShipYards!",
                    f"""
&4Player {player.id} tried to buy {unit_type} at {unit_pos}
&1There is no detected ShipYard at {unit_pos}.
Here are the player's units at that position:
{[x for x in self.game.board[unit_pos] if x.player.id == player.id]}
Here are the other player's units that position:
{[x for x in self.game.board[unit_pos] if x.player.id != player.id]}
&4They had &3{cp} cp.
                    """
                )
            elif syc[unit_pos] < unit_class.hull_size:
                self.game.throw(f"Not enough shipyard capacity!",
                    f"""
&4Player {player.id} tried to buy {unit_type} at &3{unit_pos}
&4There aren't enough shipyards &3({syc[unit_pos]} present)&4 to accomodate for that unit. &3({unit_class.hull_size} needed)
&4They had &3{cp} cp.
                    """
                )
            elif cp < (unit_cost := unit_data[unit_type]['cp_cost']):
                self.game.throw(f"Can't afford unit!",
                    f"""
&4Player {player.id} tried to buy {unit_type} at {unit_pos}
&4They had &3{cp} cp&4, which is less than the required &3{unit_cost} cp&4 to buy a {unit_type}
                    """
                )
            else:
                u = player.build_unit(self.game.unit_str_to_class(unit_type), starting_pos=unit_pos)
                self.game.log(f"They bought &2{u.get_name()}&3 for &5{u.cp_cost}")
                syc[unit_pos] -= u.hull_size

    def generate_economic_state(self):
        return [{
            'maintenance_cost': p.get_maintenance(),
            'income': p.get_income()
        } for p in self.game.players]
