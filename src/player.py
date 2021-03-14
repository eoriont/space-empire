from technology import Technology
from unit import Unit, Scout, Shipyard, ColonyShip, Colony
from unit.homeworld import Homeworld

class Player:
    @staticmethod
    def init(state: dict, player_id: int, strategy, pos: tuple):
        state["players"][player_id] = {
            "id": player_id,
            "strategy": strategy(player_id),
            "units": [],
            "home_coords": pos,
            "cp": 0 if state["game_level"] != 2 else 10,
            "technology": Technology.new_default_tech(),
            "unit_nums": {} #! To implement
        }
        Player.init_units(state, player_id)

    @staticmethod
    def init_units(state: dict, player_id: int):
        player = Player.from_id(state, player_id)
        home_coords = player["home_coords"]
        created_ids = player["units"]
        for i in range(3):
            created_ids.append(Unit.init(state, Scout, player_id, i+1, home_coords))

        if state["game_level"] > 1:
            for i in range(4):
                created_ids.append(Unit.init(state, Shipyard, player_id, i+1, home_coords))

            if state["game_level"] > 3:
                for i in range(3):
                    created_ids.append(Unit.init(state, ColonyShip, player_id, i+1, home_coords))
        player["homeworld"] = Unit.init(state, Homeworld, player_id, 1, home_coords)
        created_ids.append(player["homeworld"])

    @staticmethod
    def from_id(state: dict, player_id: int) -> dict:
        return state["players"][player_id]

    @staticmethod
    def get_units(state: dict, player_id: int) -> list:
        return [state["units"][unit_id] for unit_id in state["players"][player_id]["units"]]

    @staticmethod
    def get_homeworld(state: dict, player_id: int) -> dict:
        return Unit.from_id(state, Player.from_id(state, player_id)["homeworld"])
