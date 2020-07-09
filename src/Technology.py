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
        self[tech_type] += 1
        return self.get_price(tech_type)

    # Get the price for a certain tech
    def get_price(self, tech_type):
        level = self[tech_type]
        if tech_type == 'atk':
            return (level + 1) * 10
        elif tech_type == 'def':
            return (level + 1) * 10
        elif tech_type == 'spd':
            if level == 1:
                return 90
            elif level == 2:
                return 120
            else:
                return 10000000
        elif tech_type == 'syc':
            return level * 10
        elif tech_type == 'ss':
            return 5 + level*5

    # Return the upgradeable tech with cp
    def get_available(self, cp):
        available = []
        if self['atk'] <= 3 and cp >= self.get_price('atk'):
            available.append('atk')
        if self['def'] <= 3 and cp >= self.get_price('def'):
            available.append('def')
        if self['spd'] <= 2 and cp >= self.get_price('spd'):
            available.append('spd')
        if self['syc'] <= 3 and cp >= self.get_price('syc'):
            available.append('syc')
        if self['ss'] <= 5 and cp >= self.get_price('ss'):
            available.append('ss')
        return available

    # Return string of all the technologies
    def __str__(self):
        return ', '.join(f"|{key}: {val}|" for key, val in self.tech.items())
