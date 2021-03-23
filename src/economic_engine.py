from board import Board
from player import Player
from state import State
from technology import Technology
from unit import from_type, Unit

class EconomicEngine:
    @staticmethod
    def run_phase(state: dict):
        turn = state["turn"]
        state["phase"] = "Economic"
        state["log"].info(f"BEGINNING OF TURN {turn} ECONOMIC PHASE\n")

        for player_id in range(1, len(state["players"])+1):
            player = state["players"][player_id]
            state["current_player"] = player_id

            player["cp"] += Player.get_income(state, player_id)
            maintenance = Player.get_maintenance(state, player_id)

            while player["cp"] - maintenance < 0:
                # Do removals here
                # Remember to update maintenance as well
                pass

            player["cp"] -= maintenance

            EconomicEngine.verify_and_make_purchases(state,
                player["strategy"].decide_purchases(State.generate_hidden(state, player_id)),
                player_id)

        state["log"].info(f"END OF TURN {turn} ECONOMIC PHASE\n")

    @staticmethod
    def verify_and_make_purchases(state: dict, purchases: dict, player_id: int):
        tech_prices = State.technology_data()["technology_data"]
        player = state["players"][player_id]

        for t in purchases["technology"]:
            price = tech_prices[t][player["technology"][t]]
            if player["cp"] < price:
                state["log"].throw("Can't afford unit!")
            else:
                player["technology"][t] += 1
                player["cp"] -= price
                state["log"].info(f"Player bought some technology! {t}")

        unit_data = State.unit_data()["unit_data"]
        syc = {}
        for u in purchases["units"]:
            if u["coords"] not in syc:
                syc[u["coords"]] = Board.get_shipyard_capacity(state, u["coords"])
            unit_class = from_type(u["type"])
            if state["game_level"] in (2, 3) and u["type"] != "Scout":
                state["log"].throw("Can only buy scouts in this level of game!")
            elif player["technology"]["shipsize"] < unit_data[u["type"]]["shipsize_needed"]:
                state["log"].throw("Player bought unit without sufficient shipsize tech!")
            elif u["type"] == "Shipyard" and not Board.pos_contains(state, u["coords"], "Colony"):
                state["log"].throw("Can only build shipyards at colonies!")
            elif not Board.pos_contains(state, u["coords"], "Shipyard"):
                state["log"].throw("Can only build ships at shipyards!")
            elif syc[u["coords"]] < unit_class.hull_size:
                state["log"].throw("Not enough shipyards!")
            elif player["cp"] < unit_data[u["type"]]["cp_cost"]:
                state["log"].throw("Can't afford unit!")
            else:
                unit_id = Unit.init(state, unit_class, player_id, u["coords"])
                state["log"].info(f"Player bought {u['type']}.")
                player["cp"] -= unit_data[u["type"]]["cp_cost"]
                player["units"].append(unit_id)
                syc[u["coords"]] -= unit_class.hull_size
