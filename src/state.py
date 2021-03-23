from unit import Unit, from_type
from player import Player
from log import Log

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

    @staticmethod
    def from_standard(state: dict, strategies: list) -> dict:
        players = {
            k: {
                "cp": p["cp"],
                "id": k,
                "strategy": strategies[k-1](k),
                "technology": p["technology"],
                "homeworld": (k, "Homeworld", 1),
                "unit_nums": {},
                "units": [
                    (k, u["type"], u["num"]) for u in p["units"]
                ]
            } for k, p in state["players"].items()
        }
        units = {
            (pid, u["type"], u["num"]): {
                "type": u["type"],
                "player_id": pid,
                "num": u["num"],
                "pos": u["coords"],
                "name": f"Player {pid} {u['type']} {u['num']}",
                "technology": u["technology"],
                "armor": u["hits_left"],
                "last_turn_moved": 0,
                "maintenance_cost": from_type(u["type"]).maintenance,
            } for pid, p in state["players"].items() for u in p["units"]
        }
        for pid, p in state["players"].items():
            units[(pid, "Homeworld", 1)] = {
                "pos": p["homeworld"]["coords"],
                "type": "Homeworld",
                "armor": p["homeworld"]["hits_left"],
                "player_id": pid,
                "turn_created": 1,
                "num": 1,
                "technology": {}
            }
        board_state = {}
        for uid, u in units.items():
            unit_nums = players[uid[0]]["unit_nums"]
            if uid[1] not in unit_nums:
                unit_nums[uid[1]] = 0
            unit_nums[uid[1]] += 1
            pos = u["pos"]
            if pos not in board_state:
                board_state[pos] = []
            board_state[pos].append(uid)

        return {
            "players": players,
            "units": units,
            "board_size": state["board_size"],
            "game_level": 3,
            "winner": None,
            "turn": state["turn"],
            "phase": state["phase"],
            "round": state["round"],
            "board_state": board_state,
            "log": Log(True, True),
            "current_player": state["current_player"]
        }

    @staticmethod
    def compare_native_states(state1, state2):
        for p in state1["players"].values():
            p["units"].sort()
            p["strategy"] = type(p["strategy"]).__name__

        for val in state1["board_state"].values():
            val.sort()

        for u in state1["units"].values():
            if "last_turn_moved" in u:
                del u["last_turn_moved"]

        del state1["log"]

        for p in state2["players"].values():
            p["units"].sort()
            p["strategy"] = type(p["strategy"]).__name__

        for val in state2["board_state"].values():
            val.sort()

        for u in state2["units"].values():
            if "last_turn_moved" in u:
                del u["last_turn_moved"]

        del state2["log"]

        # Useful for debugging:
        # from pprint import pprint
        # pprint(state1)
        # pprint(state2)

        return state1 == state2
