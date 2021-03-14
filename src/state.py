from unit import Unit, from_type
from player import Player

class State:
    @staticmethod
    def generate_hidden(state: dict, player_id: int) -> dict:
        return {
            "turn": state["turn"],
            "board_size": state["board_size"],
            "phase": state["phase"],
            "round": state["round"],
            "current_player": state["current_player"],
            "winner": state["winner"],
            "players": {
                pid: State.single_player_data(state, pid, pid != player_id)
                for pid in state["players"].keys()
            },
            **State.unit_data(),
            **State.technology_data()
        }

    @staticmethod
    def single_player_data(state: dict, player_id: int, hidden: bool) -> dict:
        if hidden:
            return {
                "homeworld": State.single_unit_state(Player.get_homeworld(state, player_id), hidden),
                "units": [State.single_unit_state(unit, hidden) for unit in Player.get_units(state, player_id)
                    if Player.from_id(state, player_id)["homeworld"] != Unit.get_id(unit)]
            }
        else:
            return {
                "cp": Player.from_id(state, player_id)["cp"],
                "homeworld": State.single_unit_state(Player.get_homeworld(state, player_id), hidden),
                "units": [State.single_unit_state(unit, hidden) for unit in Player.get_units(state, player_id)
                    if Player.from_id(state, player_id)["homeworld"] != Unit.get_id(unit)]
            }

    @staticmethod
    def single_unit_state(unit: dict, hidden: bool) -> dict:
        if hidden:
            return {
                "coords": unit["pos"],
                "player": unit["player_id"],
                "num": unit["num"],
            }
        else:
            return {
                "coords": unit["pos"],
                "type": unit["type"],
                "player": unit["player_id"],
                "num": unit["num"],
                "hits_left": from_type(unit["type"]).armor - unit["armor"],
                "technology": unit["technology"].copy()
            }

    @staticmethod
    def unit_data() -> dict:
        return {
            'unit_data': {
                'Battleship': {'cp_cost': 20, 'hullsize': 3, 'shipsize_needed': 5, 'tactics': 5, 'attack': 5, 'defense': 2, 'maintenance': 3},
                'Battlecruiser': {'cp_cost': 15, 'hullsize': 2, 'shipsize_needed': 4, 'tactics': 4, 'attack': 5, 'defense': 1, 'maintenance': 2},
                'Cruiser': {'cp_cost': 12, 'hullsize': 2, 'shipsize_needed': 3, 'tactics': 3, 'attack': 4, 'defense': 1, 'maintenance': 2},
                'Destroyer': {'cp_cost': 9, 'hullsize': 1, 'shipsize_needed': 2, 'tactics': 2, 'attack': 4, 'defense': 0, 'maintenance': 1},
                'Dreadnaught': {'cp_cost': 24, 'hullsize': 3, 'shipsize_needed': 6, 'tactics': 5, 'attack': 6, 'defense': 3, 'maintenance': 3},
                'Scout': {'cp_cost': 6, 'hullsize': 1, 'shipsize_needed': 1, 'tactics': 1, 'attack': 3, 'defense': 0, 'maintenance': 1},
                'Shipyard': {'cp_cost': 3, 'hullsize': 1, 'shipsize_needed': 1, 'tactics': 3, 'attack': 3, 'defense': 0, 'maintenance': 0},
                'Decoy': {'cp_cost': 1, 'hullsize': 0, 'shipsize_needed': 1, 'tactics': 0, 'attack': 0, 'defense': 0, 'maintenance': 0},
                'Colonyship': {'cp_cost': 8, 'hullsize': 1, 'shipsize_needed': 1, 'tactics': 0, 'attack': 0, 'defense': 0, 'maintenance': 0},
                'Base': {'cp_cost': 12, 'hullsize': 3, 'shipsize_needed': 2, 'tactics': 5, 'attack': 7, 'defense': 2, 'maintenance': 0},
            }
        }

    @staticmethod
    def technology_data() -> dict:
        return {
            # Contains the price of level (index + 1)
            'technology_data': {
                'shipsize': [0, 10, 15, 20, 25, 30],
                'attack': [20, 30, 40],
                'defense': [20, 30, 40],
                'movement': [0, 20, 30, 40, 40, 40],
                'shipyard': [0, 20, 30]
            }
        }
