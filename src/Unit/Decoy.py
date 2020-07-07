from Unit.Unit import Unit


class Decoy(Unit):
    cp_cost = 1
    armor = 0

    def __init__(self, *args):
        super().__init__(*args)
        self.maitenance_cost = 0
