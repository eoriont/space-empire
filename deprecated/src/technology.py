class Technology:
    def __init__(self, tech, default_tech=None):
        if default_tech is None:
            #! Not sure if atk and def start at 0 + mov, ss, sy start at 1
            default_tech = {}
        if type(default_tech) == Technology:
            default_tech = default_tech.tech
        self.tech = default_tech
        self.tech.update(tech)

    def copy(self):
        return Technology(self.tech.copy())

    # Get tech level
    def __getitem__(self, tech_type):
        return self.tech[tech_type]

    # Set tech level
    def __setitem__(self, tech_type, new_level):
        self.tech[tech_type] = new_level

    # Add 1 to tech level and return price
    def buy_tech(self, tech_type):
        price = Technology.get_state()[tech_type][self[tech_type]]
        self[tech_type] += 1
        return price

    @staticmethod
    def get_state():
        return {
            "shipsize": [0, 10, 15, 20, 25, 30],
            "attack": [20, 30, 40],
            "defense": [20, 30, 40],
            "movement": [0, 20, 30, 40, 40, 40],
            "shipyard": [0, 20, 30],
            "terraform": [], # Unimplemented
            "tactics": []    # Unimplemented
        }

    def get_obj_state(self):
        return {
            'attack': self['attack'],
            'defense': self['defense'],
            'movement': self['movement'],
            'shipsize': self["shipsize"],
            'shipyard': self["shipyard"],
            'terraform': self["terraform"], # Unimplemented
            'tactics': self['tactics']      # Unimplemented
        }

    def get_spaces(self):
        spaces_per_phase = [
            (1, 1, 1),
            (1, 1, 2),
            (1, 2, 2),
            (2, 2, 2),
            (2, 2, 3),
            (2, 3, 3),
        ]
        return spaces_per_phase[self['movement']]

    # Return string of all the technologies
    def __str__(self):
        return ', '.join(f"|{key}: {val}|" for key, val in self.tech.items())
