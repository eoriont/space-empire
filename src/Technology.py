
class Technology:
    # Initialize the tech
    def __init__(self, attack=0, defense=0, speed=0, shipyard=1, ship_size=1):
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.shipyard = shipyard
        self.ship_size = ship_size

    # Add tech levels from 2 different tech instances
    @staticmethod
    def combine_tech(t1, t2):
        return Technology(t1.attack + t2.attack, t1.defense + t2.defense, t1.speed+t2.speed, t1.shipyard+t2.shipyard)

    # Return the upgradeable tech with cp
    def get_available(self, cp):
        available = []
        if self.attack <= 3 and cp >= self.get_price('atk'):
            available.append('atk')
        if self.defense <= 3 and cp >= self.get_price('def'):
            available.append('def')
        if self.speed <= 2 and cp >= self.get_price('spd'):
            available.append('spd')
        if self.shipyard <= 3 and cp >= self.get_price('sy'):
            available.append('sy')
        if self.ship_size <= 5 and cp >= self.get_price('ss'):
            available.append('ss')
        return available

    # Get the price for a certain tech
    def get_price(self, tech_type):
        if tech_type == 'atk':
            return (self.attack + 1) * 10
        elif tech_type == 'def':
            return (self.defense + 1) * 10
        elif tech_type == 'spd':
            if self.speed == 1:
                return 90
            elif self.speed == 2:
                return 120
            else:
                return 10000000
        elif tech_type == 'sy':
            return self.shipyard * 10
        elif tech_type == 'ss':
            return 5 + self.ship_size*5

    # Add 1 to tech level and return price
    def buy_tech(self, tech_type):
        price = self.get_price(tech_type)
        if tech_type == 'atk':
            self.attack += 1
        elif tech_type == 'def':
            self.defense += 1
        elif tech_type == 'spd':
            self.speed += 1
        elif tech_type == 'sy':
            self.shipyard += 1
        elif tech_type == 'ss':
            self.ship_size += 1
        return price

    # Return string of all the technologies
    def __str__(self):
        return f"Speed: {self.speed}, Attack: {self.attack}, Defense: {self.defense}"
