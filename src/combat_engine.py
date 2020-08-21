
import random
from unit.decoy import Decoy
from unit.colony_ship import Colonyship


class CombatEngine:

    def __init__(self, game):
        self.game = game

    def battle(self, units):
        units = self.remove_units(units)

        # Sort units by attack class, and by player
        units = sorted(units, key=lambda x: x.player.id)
        units = sorted(units, key=lambda x: ord(x.attack_class or 'Z'))

        for u in self.get_screen_units(units):
            units.remove(u)

        # Loop through units in the correct attack order and battle
        while not CombatEngine.units_on_same_team(units):
            for unit in units:
                if unit.no_attack:
                    continue
                attack_options = [u for u in units if u.player !=
                                  unit.player and u.alive]
                if len(attack_options) == 0 or not unit.alive:
                    continue
                unit2 = unit.player.choose_unit_to_attack(attack_options)
                self.duel(unit, unit2)

    def get_screen_units(self, units):
        punits = CombatEngine.sort_units_by_player(units)
        # If a player has more units than the other, screen
        if len(set(punits.values())) <= 1:
            return self.game.players[max(punits, key=punits.get)].screen_units()
        return []

    # Remove decoys/colonyships
    def remove_units(self, units):
        for u in units:
            if type(u) in [Decoy, Colonyship]:
                u.destroy("combat")
        return [u for u in units if u.alive]

    # A duel between an attacker and a defender
    def duel(self, attacker, defender):
        atk_str = attacker.attack_strength + attacker.tech['atk']
        def_str = defender.defense_strength + defender.tech['def']
        hit_threshold = atk_str - def_str
        die_roll = self.game.die_roll()
        if die_roll <= hit_threshold or die_roll == 1:
            defender.hurt(attacker.name)

    # Return dictionary of players and their units in a unit list
    @staticmethod
    def sort_units_by_player(units):
        lens = {}
        for unit in units:
            pid = unit.player.id
            if pid not in lens.keys():
                lens[pid] = 0
            lens[pid] += 1
        return lens

    # Return if all the units in the given list belong to the same player
    @staticmethod
    def units_on_same_team(units):
        players = [
            unit.player for unit in units if unit.alive and not unit.no_attack]
        if len(players) == 0:
            return True
        return players.count(players[0]) == len(players)
