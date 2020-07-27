
import random
from unit.decoy import Decoy


class CombatEngine:

    def __init__(self, game):
        self.game = game

    def unit_battle(self, units):
        # Remove decoys
        for u in units:
            if type(u) == Decoy:
                u.destroy()
                units.remove(u)
        # Sort units by attack class, and by player
        units = sorted(units, key=lambda x: ord(x.attack_class or 'Z'))
        player_units = CombatEngine.sort_units_by_player(units)
        player_units_amounts = {name: len(players_units)
                                for name, players_units in player_units.items()}
        # If a player has more units than the other, screen
        if len(set(player_units_amounts.values())) <= 1:
            player_with_more_units_name = max(
                player_units_amounts, key=player_units_amounts.get)
            # nums = unit_nums[:2] if unit_nums[0] < unit_nums[1] else unit_nums[:2][::-1]
            # num_units_to_screen = random.randint(*nums)
            # units_to_screen = random.sample(
            #     player_units[player_with_more_units], num_units_to_screen)
            units_to_screen = self.game.players_by_name[player_with_more_units_name].screen_units(
            )
            for u in units_to_screen:
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
                u1_atk_str = unit.attack_strength + unit.tech['atk']
                u2_def_str = unit2.defense_strength + unit2.tech['def']
                hit_threshold = u1_atk_str - u2_def_str
                die_roll = random.randint(0, 6)
                if die_roll <= hit_threshold or die_roll == 1:
                    unit2.hurt()
                    self.game.log(f"{unit2.name} has been hurt by {unit.name}")

    # Return dictionary of players and their units in a unit list
    @staticmethod
    def sort_units_by_player(units):
        new_units = {}
        for unit in units:
            if unit.player.name in new_units.keys():
                new_units[unit.player.name].append(unit)
            else:
                new_units[unit.player.name] = [unit]
        return new_units

    # Return if all the units in the given list belong to the same player
    @staticmethod
    def units_on_same_team(units):
        players = [
            unit.player for unit in units if unit.alive and not unit.no_attack]
        if len(players) == 0:
            return True
        return players.count(players[0]) == len(players)
