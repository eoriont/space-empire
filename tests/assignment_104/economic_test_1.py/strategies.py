class Strategy1:
    def __init__(self, player_num):
        self.player_num = player_num

    def decide_purchases(self, state):
        home_coords = state["players"][self.player_num]["homeworld"]["coords"]
        return {
            "technology": ["attack"],
            "units": [
                {
                    "type": "Scout",
                    "coords": home_coords
                }
            ]
        }

class Strategy2:
    def __init__(self, player_num):
        self.player_num = player_num

    def decide_purchases(self, state):
        home_coords = state["players"][self.player_num]["homeworld"]["coords"]
        return {
            "technology": ["defense"],
            "units": [
                {
                    "type": "Scout",
                    "coords": home_coords
                }
            ]*2
        }
