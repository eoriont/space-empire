
import random
from unit import Decoy, ColonyShip


class CombatEngine:

    def __init__(self, game):
        self.game = game

    def battle(self, pos):
        # Loop through units in the correct attack order and battle
        units = [self.state_to_unit(u) for u in self.generate_combat_array(pos)]
        while CombatEngine.is_battle(units):
            for attacker in units:
                cbt_arr = self.generate_combat_array(pos)

                if attacker.no_attack or not attacker.alive:
                    continue

                # If only the attacker is in cbt_arr, then there's no battle
                if len(cbt_arr) <= 1 or pos not in self.get_combat_positions():
                    continue

                self.game.current_player_id = attacker.player.id
                # I pass in the fake dict because there might not be a point for the whole cbt_arr
                defender_state = attacker.player.strat.decide_which_unit_to_attack(
                    self.generate_combat_array(), pos, attacker.id)

                defender = self.state_to_unit(cbt_arr[defender_state])
                self.duel(attacker, defender)

            units = [self.state_to_unit(u) for u in self.generate_combat_array(pos)]

    # Unit state -> unit class
    def state_to_unit(self, unit):
        return self.game.players[unit['player']].units[unit['id']]

    # A duel between an attacker and a defender
    def duel(self, attacker, defender):
        atk_str = attacker.attack_strength + attacker.tech['attack']
        def_str = defender.defense_strength + defender.tech['defense']
        hit_threshold = atk_str - def_str
        die_roll = self.game.die_roll()
        if die_roll <= hit_threshold or die_roll == 1:
            defender.hurt(attacker.id)

    # Return if all the units in the given list belong to the same player
    @staticmethod
    def is_battle(units):
        if len(units) == 0:
            return False
        players = [
            unit.player for unit in units if unit.alive and not unit.no_attack]
        return players.count(players[0]) != len(players)

    # Resolve combat between all units
    def combat_phase(self, current_turn):
        self.game.phase = "Combat"
        combat_arr = self.generate_combat_array()
        for pos in self.get_combat_positions():
            self.battle(pos)
        self.game.board.create()

    def generate_combat_array(self, pos=None):
        if pos is None:
            return {
                pos: [u.generate_state() for u in self.order_ships(units)]
                 for pos, units in self.game.board.items()
                if CombatEngine.is_battle(units)
            }
        else:
            return [u.generate_state() for u in self.order_ships(self.game.board[pos])]

    def get_combat_positions(self):
        return [pos for pos, units in self.game.board.items() if CombatEngine.is_battle(units)]

    def order_ships(self, ships):
        for u in ships:
            if type(u) in [Decoy, ColonyShip]:
                u.destroy("combat")
        ships = [u for u in ships if u.alive]

        # Sort units by attack class, and by player
        #! This would be changed to tactics technology and attacker/defender
        ships = sorted(ships, key=lambda x: (
            ord(x.attack_class or 'Z'), x.player.id))

        # Screen Units
        pids = [u.player.id for u in ships]
        units_per_player = {pid: pids.count(pid) for pid in set(pids)}
        favored_player = self.game.players[max(units_per_player, key=units_per_player.get)]

        # If a player has more units than the other, screen
        if len(set(units_per_player.values())) <= 1:
            #! Generate a state to screen instead of this little dictionary
            screen_units = favored_player.strat.decide_which_units_to_screen(units_per_player)
            return [s for s in ships if s not in screen_units]

        return ships
