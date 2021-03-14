from types import LambdaType

class Board:
    @staticmethod
    def is_in_bounds(state: dict, pos: tuple) -> bool:
        x, y = pos
        a, b = state["board_size"]
        return 0 <= x < a and 0 <= y < b

    @staticmethod
    def ensure_pos(state: dict, pos: tuple) -> None:
        if pos not in state["board_state"]:
            state["board_state"][pos] = []

    @staticmethod
    def move_unit(state: dict, unit_id: int, old_pos: tuple, new_pos: tuple) -> None:
        Board.ensure_pos(state, new_pos)
        state["board_state"][old_pos].remove(unit_id)
        state["board_state"][new_pos].append(unit_id)

    @staticmethod
    def remove_unit(state: dict, unit_id: int) -> None:
        unit = state["units"][unit_id]
        state["board_state"][unit["pos"]].remove(unit_id)

    @staticmethod
    def new_unit(state: dict, unit_id: int, pos: tuple) -> None:
        Board.ensure_pos(state, pos)
        state["board_state"][pos].append(unit_id)

    @staticmethod
    def get_units(state: dict, pos: tuple) -> list:
        return [state["units"][i] for i in state["board_state"][pos]]

    @staticmethod
    def get_unit_ids(state: dict, pos: tuple) -> list:
        return state["board_state"][pos]

    @staticmethod
    def filter_units(state: dict, pos: tuple, filter: LambdaType = lambda _: True, map: LambdaType = lambda x: x) -> list:
        return [map(u) for u in Board.get_units(state, pos) if filter(u)]

    @staticmethod
    def is_battle(state: dict, pos: tuple) -> list:
        unit_owners = Board.filter_units(state, pos, map = lambda x: x["player_id"])
        return len(set(unit_owners)) > 1

    @staticmethod
    def get_combat_positions(state: dict) -> list:
        return [pos for pos in state["board_state"].keys() if Board.is_battle(state, pos)]
