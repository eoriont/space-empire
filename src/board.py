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
    def move_unit(state: dict, unit_id: tuple, old_pos: tuple, new_pos: tuple) -> None:
        Board.ensure_pos(state, new_pos)
        state["board_state"][old_pos].remove(unit_id)
        state["board_state"][new_pos].append(unit_id)

        # This makes a new number for every movement subphase and every player
        state["units"][unit_id]["last_turn_moved"] = (state["round"]-1)*(state["turn"]*6)+(state["current_player"]-1)

    @staticmethod
    def remove_unit(state: dict, unit: dict) -> None:
        state["board_state"][unit["pos"]].remove((unit["player_id"], unit["type"], unit["num"]))

    @staticmethod
    def new_unit(state: dict, unit_id: tuple, pos: tuple) -> None:
        Board.ensure_pos(state, pos)
        state["board_state"][pos].append(unit_id)

    @staticmethod
    def get_units(state: dict, pos: tuple) -> list:
        Board.ensure_pos(state, pos)
        return [state["units"][i] for i in state["board_state"][pos]]

    @staticmethod
    def get_unit_ids(state: dict, pos: tuple) -> list:
        Board.ensure_pos(state, pos)
        return state["board_state"][pos]

    @staticmethod
    def filter_units(state: dict, pos: tuple, filter: LambdaType = lambda _: True, map: LambdaType = lambda x: x) -> list:
        Board.ensure_pos(state, pos)
        return [map(u) for u in Board.get_units(state, pos) if filter(u)]

    @staticmethod
    def is_battle(state: dict, pos: tuple) -> list:
        unit_owners = Board.filter_units(state, pos, map = lambda x: x["player_id"])
        return len(set(unit_owners)) > 1

    @staticmethod
    def get_combat_positions(state: dict) -> list:
        return [pos for pos in state["board_state"].keys() if Board.is_battle(state, pos)]

    @staticmethod
    def pos_contains(state: dict, pos: tuple, unit_type: str):
        return any(Board.filter_units(state, pos, filter = lambda x: x["type"] == unit_type, map = lambda x: True))

    @staticmethod
    def get_shipyard_capacity(state: dict, pos: tuple):
        #! This doesn't account for shipyard technology
        return len(Board.filter_units(state, pos, filter = lambda x: x["type"] == "Shipyard"))

    @staticmethod
    def clean(state: dict) -> None:
        for pos in list(state["board_state"].keys()):
            if len(state["board_state"][pos]) == 0:
                del state["board_state"][pos]
