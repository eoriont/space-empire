class Technology:
    def __init__(self, tech, default_tech=None):
        if default_tech is None:
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
        if tech_type == 'atk':
            return (level + 1) * 10
        elif tech_type == 'def':
            return (level + 1) * 10
        elif tech_type == 'mov':
            if level == 1:
                return 20
            elif level == 2:
                return 30
            elif level in [3, 4, 5]:
                return 40
        elif tech_type == 'syc':
            return level * 10
        elif tech_type == 'ss':
            return 5 + level*5

    def get_state(self):
        return {
            "ss": {
                "price": [5, 10, 15, 20, 25]
            }
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
        return spaces_per_phase[self.tech['mov']]

    # Return the upgradeable tech with cp
    def get_available(self, cp):
        available = []
        if self['atk'] <= 3 and cp >= self.get_price('atk'):
            available.append('atk')
        if self['def'] <= 3 and cp >= self.get_price('def'):
            available.append('def')
        if self['mov'] <= 5 and cp >= self.get_price('mov'):
            available.append('mov')
        if self['syc'] <= 3 and cp >= self.get_price('syc'):
            available.append('syc')
        if self['ss'] <= 5 and cp >= self.get_price('ss'):
            available.append('ss')
        return available

    # Return string of all the technologies
    def __str__(self):
        return ', '.join(f"|{key}: {val}|" for key, val in self.tech.items())
