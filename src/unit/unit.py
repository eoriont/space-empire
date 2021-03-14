from board import Board
from technology import Technology
from win_exception import WinException

class Unit:
    armor = 0
    hull_size = 0
    no_maintenance = False
    no_attack = False
    attack_class = None
    immovable = False
    attack_class = "Z"

    @staticmethod
    def init(state: dict, unit_type: "Unit", player_id: int, num: int, pos: tuple, extra_data: dict = None) -> int:
        if extra_data is None:
            extra_data = {}
        id = (player_id, unit_type.name, num)
        state["units"][id] = {
            "type": unit_type.name,
            "player_id": player_id,
            "num": num,
            "pos": pos,
            "name": f"Player {player_id} {unit_type.name} {num}",
            "technology": Technology.copy_player_tech(state, player_id),
            "armor": unit_type.armor,
            **extra_data
        }

        # Each player only has 1 homeworld
        if unit_type.name == "Homeworld":
            state["units"][id]["name"] = f"Player {player_id} Homeworld"

        Board.new_unit(state, id, pos)
        return id

    @staticmethod
    def hurt(state: dict, attacker_id: tuple, defender_id: tuple) -> None:
        attacker = state["units"][attacker_id]
        defender = state["units"][defender_id]

        defender["armor"] -= 1
        if defender["armor"] <= 0:
            state["log"].info(f"\t\t{defender['name']} was destroyed\n")

            if defender["type"] == "Homeworld":
                state["winner"] = attacker["player_id"]

            Unit.destroy(state, defender_id)

            if state["winner"]:
                raise WinException("We have a winner! Exit now...")

    @staticmethod
    def destroy(state: dict, unit_id: tuple) -> None:
        unit = Unit.from_id(state, unit_id)
        Board.remove_unit(state, unit)
        state["players"][unit["player_id"]]["units"].remove(unit_id)
        del state["units"][unit_id]

    @staticmethod
    def ids_to_units(state: dict, unit_ids: list) -> list:
        return [state["units"][id] for id in unit_ids]

    @staticmethod
    def from_id(state: dict, unit_id: tuple) -> dict:
        return state["units"][unit_id]

    @staticmethod
    def get_id(unit: dict) -> tuple:
        return unit["player_id"], unit["type"], unit["num"]
