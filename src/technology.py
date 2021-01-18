class Technology:
    def __init__(self, tech, default_tech=None):
        if default_tech is None:
            #! Not sure if atk and def start at 0 + mov, ss, sy start at 1
            default_tech = {}
        if type(default_tech) == Technology:
            default_tech = default_tech.tech
        self.tech = default_tech
        self.tech.update(tech)

    # Get tech level
    def __getitem__(self, tech_type):
        return self.tech[tech_type]

    # Set tech level
    def __setitem__(self, tech_type, new_level):
        self.tech[tech_type] = new_level

    # Add 1 to tech level and return price
    def buy_tech(self, tech_type):
        price = self.get_price(tech_type)
        self[tech_type] += 1
        return price

    # Get the price for a certain tech
    def get_price(self, tech_type):
        level = self[tech_type]
        if tech_type == 'attack':
            return (level + 1) * 10
        elif tech_type == 'defense':
            return (level + 1) * 10
        elif tech_type == 'movement':
            if level == 1:
                return 20
            elif level == 2:
                return 30
            elif level in [3, 4, 5]:
                return 40
        elif tech_type == 'shipyard':
            return level * 10
        elif tech_type == 'shipsize':
            return 5 + level*5

    @staticmethod
    def get_state():
        # TODO: Change get_price to reflect this
        return {
            "shipsize": [5, 10, 15, 20, 25],
            "attack": [20, 30, 40],
            "defense": [20, 30, 40],
            "movement": [20, 30, 40, 40, 40],
            "shipyard": [20, 30]
        }

    def get_obj_state(self):
        return {
            'attack': self['attack'],
            'defense': self['defense'],
            'movement': self['movement']
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
        return spaces_per_phase[self.tech['movement']]

    # Return the upgradeable tech with cp
    def get_available(self, cp):
        available = []
        if self['attack'] <= 3 and cp >= self.get_price('attack'):
            available.append('attack')
        if self['defense'] <= 3 and cp >= self.get_price('defense'):
            available.append('defense')
        if self['movement'] <= 5 and cp >= self.get_price('movement'):
            available.append('movement')
        if self['shipyard'] <= 3 and cp >= self.get_price('shipyard'):
            available.append('shipyard')
        if self['shipsize'] <= 5 and cp >= self.get_price('shipsize'):
            available.append('shipsize')
        return available

    # Return string of all the technologies
    def __str__(self):
        return ', '.join(f"|{key}: {val}|" for key, val in self.tech.items())
