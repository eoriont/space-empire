from board import Board
from state import State
from technology import Technology
from unit import Unit, from_type

class MovementEngine:
    @staticmethod
    def run_phase(state: dict):
        turn = state["turn"]
        state["phase"] = "Movement"
        state["log"].info(f"BEGINNING OF TURN {turn} MOVEMENT PHASE")

        rounds = 1 if state["game_level"] <= 2 else 3

        for subphase in range(rounds):
            state["round"] = subphase+1
            state["log"].info(f"\n\tMovement Round {subphase+1}")

            for player in state["players"].values():
                state["current_player"] = player["id"]
                for unit_id in player["units"]:
                    unit = Unit.from_id(state, unit_id)

                    if from_type(unit["type"]).immovable:
                        continue

                    old_pos = unit["pos"]
                    translation = player["strategy"].decide_ship_movement(unit["type"], unit["num"], State.generate_hidden(state, player["id"]))

                    if translation != (0, 0):
                        new_pos = (old_pos[0] + translation[0], old_pos[1] + translation[1])
                        state["log"].info(f"\t\t{unit['name']}: {old_pos} -> {new_pos}")
                        MovementEngine.validate_and_move(state, unit_id, translation, subphase)

        state["log"].info("\n\tEnding Unit Locations\n")
        for player in state["players"].values():
            for unit_id in player["units"]:
                unit = state["units"][unit_id]
                state["log"].info(f"\t\t{unit['name']}: {unit['pos']}")
            state["log"].info("")

        Board.clean(state)

        state["round"] = None
        state["log"].info(f"END OF TURN {turn} MOVEMENT PHASE\n")

    @staticmethod
    def validate_and_move(state: dict, unit_id: tuple, translation: tuple, subphase: int):
        unit = Unit.from_id(state, unit_id)
        tech_spaces = Technology.get_movement_spaces(unit["technology"], subphase)
        is_possible = translation[0] + translation[1] <= tech_spaces

        old_pos = unit["pos"]
        new_pos = (old_pos[0] + translation[0], old_pos[1] + translation[1])

        in_bounds = Board.is_in_bounds(state, new_pos)

        if not (is_possible and in_bounds):
            state["log"].throw("Invalid Move!")
        else:
            unit["pos"] = new_pos
            Board.move_unit(state, unit_id, old_pos, new_pos)
