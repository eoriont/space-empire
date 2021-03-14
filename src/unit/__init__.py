# Unit comes first
from unit.unit import Unit

from unit.scout import Scout
from unit.dreadnaught import Dreadnaught
from unit.destroyer import Destroyer
from unit.decoy import Decoy
from unit.cruiser import Cruiser
from unit.battle_cruiser import BattleCruiser
from unit.base import Base
from unit.shipyard import Shipyard
from unit.colony import Colony
from unit.colony_ship import ColonyShip
from unit.homeworld import Homeworld

def from_type(unit_type: str):
    return {
        "Scout": Scout,
        "Dreadnaught": Dreadnaught,
        "Destroyer": Destroyer,
        "Decoy": Decoy,
        "Cruiser": Cruiser,
        "BattleCruiser": BattleCruiser,
        "Base": Base,
        "Shipyard": Shipyard,
        "Colony": Colony,
        "ColonyShip": ColonyShip,
        "Homeworld": Homeworld
    }[unit_type]
