
import random
from unit.decoy import Decoy
from unit.colony_ship import Colonyship


class CombatEngine:

    def __init__(self, game):
        self.game = game

    def battle(self, units, pos):
        # Loop through units in the correct attack order and battle
        u2s = [self.state_to_unit(u) for u in units]
        #! Lord forgive me for this awful inefficient garbage
        while not CombatEngine.units_on_same_team(u2s):
            for i, unit in enumerate(units):
                cbt_arr = self.generate_combat_array()
                if pos not in cbt_arr:
                    return
                us = cbt_arr[pos]
                unit_obj = self.state_to_unit(unit)
                if unit_obj.no_attack or not unit_obj.alive:
                    continue
                attack_options = [u for u in us if u['player']
                                  != unit['player'] and u['alive']]
                if len(attack_options) == 0:
                    continue
                self.game.current_player_id = unit['id']
                unit2 = unit_obj.player.strat.decide_which_unit_to_attack(
                    us, pos, i)
                unit2_obj = self.state_to_unit(us[unit2])
                self.duel(unit_obj, unit2_obj)

    def get_screen_units(self, units):
        punits = CombatEngine.sort_units_by_player(units)
        # If a player has more units than the other, screen
        if len(set(punits.values())) <= 1:
            return self.game.players[max(punits, key=punits.get)-1].strat.decide_which_units_to_screen(punits)
        return []

    # Turn unit + player id into class
    def state_to_unit(self, unit):
        #! This exception is bad and is a hack -- it should be changed
        try:
            return self.game.players[unit['player']].units[unit['unit']]
        except IndexError:
            return None

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
            defender.hurt(attacker.id)

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

    # Resolve combat between all units
    def combat_phase(self, current_turn):
        self.game.phase = "Combat"
        combat_arr = self.generate_combat_array()
        for pos, units in combat_arr.items():
            self.battle(units, pos)
        self.destroy_dead_units()
        self.game.board.create()
        self.game.render()

    def destroy_dead_units(self):
        for p in self.game.players:
            for u in p.units:
                if not u.alive:
                    u.destroy()

    def generate_combat_array(self):
        return {
            pos: [
                {'player': u.player.id-1,
                 'unit': u.player.units.index(u),
                 'alive': u.alive, 'type': type(u).__name__,
                 'id': i}
                for i, u in enumerate(self.order_ships(units))
            ] for pos, units in self.game.board.items()
            if not CombatEngine.units_on_same_team(units)
        }

    def order_ships(self, ships):
        ships = self.remove_units(ships)

        # Sort units by attack class, and by player
        ships = sorted(ships, key=lambda x: (
            ord(x.attack_class or 'Z'), x.player.id))

        for u in self.get_screen_units(ships):
            ships.remove(u)

        return ships
