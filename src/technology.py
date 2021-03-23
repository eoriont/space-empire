class Technology:
    @staticmethod
    def get_movement_spaces(tech: dict, subphase: int):
        return (
            (1, 1, 1),
            (1, 1, 2),
            (1, 2, 2),
            (2, 2, 2),
            (2, 2, 3),
            (2, 3, 3),
        )[tech['movement']][subphase]

    @staticmethod
    def copy_player_tech(state: dict, player_id: int) -> dict:
        return state["players"][player_id]["technology"].copy()

    @staticmethod
    def copy_unit_tech(state: dict, unit_id: int) -> dict:
        return state["units"][unit_id]["technology"].copy()

    @staticmethod
    def new_default_tech():
        # The following are the starting levels for each technology level
        # Note that some do, in fact, start at 1.
        return {
            "attack": 0,
            "defense": 0,
            "movement": 1,
            "shipyard": 1,
            "shipsize": 1,
            "terraform": 0,
            "tactics": 0
        }

    @staticmethod
    def get_prices():
        return {
            "shipsize": [0, 10, 15, 20, 25, 30],
            "attack": [20, 30, 40],
            "defense": [20, 30, 40],
            "movement": [0, 20, 30, 40, 40, 40],
            "shipyard": [0, 20, 30],
            "terraform": [], # Unimplemented
            "tactics": []    # Unimplemented
        }
