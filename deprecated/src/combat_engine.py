from unit import Decoy, ColonyShip, Colony

class CombatEngine:
    def __init__(self, game):
        self.game = game

    # Returns if a home colony was destroyed
    def battle(self, pos):
        self.game.log("Combat order: " + str([u['id'] for u in self.generate_combat_array()[pos]]))
        units = [self.state_to_unit(u) for u in self.generate_combat_array()[pos]]
        self.game.log("Going into battle: " + str([(type(u).__name__, u.player.id) for u in self.game.board[pos] if u.id in u.player.units]))

        # Battle until all units are on the same team
        while CombatEngine.is_battle(units):

            # units is in combat order, so loop through as attacker
            for attacker in units:
                # Units that can't attack shouldn't be considered
                if attacker.no_attack or not attacker.alive:
                    continue

                # Generate a new array since each battle will change the contents
                cbt_arr = self.generate_combat_array()

                # If only the attacker is in cbt_arr, then there's no battle
                if len(cbt_arr) <= 1 or pos not in self.get_combat_positions():
                    continue

                # Attack!
                self.game.current_player_id = attacker.player.id

                defender_id = attacker.player.strat.decide_which_unit_to_attack(
                    cbt_arr,
                    pos,
                    cbt_arr.index(attacker.generate_state(False, True))
                )

                defender = self.state_to_unit(cbt_arr[defender_id])
                if type(defender) == Colony and len([type(x) == Colony for x in units if x.player == defender.player.id]):
                    self.game.throw("Can't attack colony while other units are present!",
f"""
&4Player {attacker.player.id} tried to attack the other player's colony, but other units were there!
""")

                # Duel returns if a home colony was destroyed
                if self.duel(attacker, defender):
                    return True

            # Reset units, since it was changed in battle
            units = [self.state_to_unit(u) for u in self.generate_combat_array()]

        self.game.log("Survivors: " + str([(type(u).__name__, u.player.id) for u in self.game.board[pos] if u.id in u.player.units]))

    # Unit state -> unit class
    def state_to_unit(self, unit):
        return self.game.players[unit['player']].units[unit['id']]

    # A duel between an attacker and a defender
    # Returns True if a home colony is defeated
    def duel(self, attacker, defender):
        atk_str = attacker.attack_strength + attacker.tech['attack']
        def_str = defender.defense_strength + defender.tech['defense']
        hit_threshold = atk_str - def_str
        die_roll = self.game.die_roll()
        self.game.log("Die was rolled: " + str(die_roll))

        # Checks if attack hits
        if die_roll <= hit_threshold or die_roll == 1:
            self.game.log(f"{attacker.get_name()} &2attacks&3 {defender.get_name()} &7at {attacker.pos}, threshold: {(hit_threshold, attacker.tech['attack'], defender.tech['defense'])}")
            defender.hurt(attacker.get_name())
            if type(defender) == Colony and defender.is_home_colony:
                return True
        else:
            self.game.log(f"{attacker.get_name()} &5misses&3 {defender.get_name()} &7at {attacker.pos}, threshold: {(hit_threshold, attacker.tech['attack'])}")


    # Return if all the units in the given list belong to the same player
    @staticmethod
    def is_battle(units):
        if len(units) == 0:
            return False
        players = [
            unit.player for unit in units if unit.alive]
        return players.count(players[0]) != len(players)

    # Resolve combat between all units
    # Returns if a home colony was destroyed
    def combat_phase(self, current_turn):
        self.game.phase = "Combat"

        # Each position in combat array has enemy units
        for pos in self.get_combat_positions():
            if self.battle(pos):
                return True

        # Make sure to update the board afterwards
        self.game.board.create()

    # Generate a state array filled with hidden units
    def generate_combat_array(self):
        # This if statement will truncate unit information based on player
        return {
            pos: [u.generate_state(True, True) for u in self.order_ships(units)]
             for pos, units in self.game.board.items()
            if CombatEngine.is_battle(units)
        }

    # Returns all positions where a battle should take place
    def get_combat_positions(self):
        return [pos for pos, units in self.game.board.items() if CombatEngine.is_battle(units)]

    # Orders a given array of ships by attack class and player
    #! Should later do tactics technology as well
    def order_ships(self, ships):
        # Destroy ships that don't participate in combat
        for u in ships:
            if type(u) in [Decoy, ColonyShip]:
                u.destroy("combat")

        # This just removes those ships above ^^
        ships = [u for u in ships if u.alive]

        # Sort units by attack class, and by player
        #! This would be changed to tactics technology and attacker/defender
        ships = sorted(ships, key=lambda x: (
            ord(x.attack_class or 'Z'), x.player.id))

        # If a player has more units than the other, screen
        if self.state["game_level"] > 3:
            # Screen Units
            pids = [u.player.id for u in ships]
            units_per_player = {pid: pids.count(pid) for pid in set(pids)}
            favored_player = self.game.players[max(units_per_player, key=units_per_player.get)]

            if len(set(units_per_player.values())) <= 1:
                #! Generate a state to screen instead of this little dictionary
                screen_units = favored_player.strat.decide_which_units_to_screen(units_per_player)
                return [s for s in ships if s not in screen_units]

        return ships
