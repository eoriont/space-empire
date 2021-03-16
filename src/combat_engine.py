from board import Board
from unit import Unit, from_type
from technology import Technology

class CombatEngine:
    @staticmethod
    def run_phase(state: dict):
        turn = state["turn"]
        state["phase"] = "Combat"
        state["log"].info(f"BEGINNING OF TURN {turn} COMBAT PHASE\n")

        combat_positions = Board.get_combat_positions(state)
        if len(combat_positions) > 0:
            # Log initial combat locations
            state["log"].info("\tCombat Locations:\n")
            for pos in combat_positions:
                state["log"].info("\t\t"+str(pos)+"\n")
                #! Do something smart to cache the order for later
                for unit_id in CombatEngine.order(state, pos):
                    state["log"].info("\t\t\t" + Unit.from_id(state, unit_id)["name"])
                state["log"].info("")

            # Actually do the combat
            for pos in combat_positions:
                state["log"].info(f"\tCombat at {str(pos)}\n ")
                CombatEngine.destroy_non_combat_units(state, pos)
                while Board.is_battle(state, pos):
                    CombatEngine.battle(state, pos)

            # Log survivors
            state["log"].info("\tSurvivors:\n")
            for pos in combat_positions:
                state["log"].info("\t\t"+str(pos)+"\n")
                for unit_id in CombatEngine.order(state, pos):
                    state["log"].info("\t\t\t" + Unit.from_id(state, unit_id)["name"])
                state["log"].info("")

        state["log"].info(f"END OF TURN {turn} COMBAT PHASE\n")

    @staticmethod
    def battle(state: dict, pos: tuple):
        unit_ids = CombatEngine.order(state, pos)

        for attacker_id in unit_ids:
            # If the unit was killed
            if attacker_id not in state["units"]:
                continue

            attacker = state["units"][attacker_id]
            # If the unit can't attack
            if from_type(attacker["type"]).no_attack:
                continue

            state["current_player"] = attacker["player_id"]
            attacking_player = state["players"][attacker["player_id"]]

            #! This could be more efficient
            if not Board.is_battle(state, pos):
                break

            #! I don't like this because it has a bunch of extra looping
            combat_state = CombatEngine.generate_combat_state(state)

            defender_id = attacking_player["strategy"].decide_which_unit_to_attack(
                combat_state, pos, attacker["type"], attacker["num"]
            )

            killed = CombatEngine.duel(state, attacker_id, defender_id)
            if killed is not None:
                unit_ids.remove(killed)

    @staticmethod
    def duel(state: dict, attacker_id: int, defender_id: int):
        attacker = state["units"][attacker_id]
        defender = state["units"][defender_id]
        attack_threshold = from_type(attacker["type"]).attack_strength + attacker["technology"]["attack"]
        defense_threshold = from_type(defender["type"]).defense_strength + defender["technology"]["defense"]
        hit_threshold = attack_threshold - defense_threshold
        die_roll = state["die_roll"]()

        state["log"].info(f"\t\tAttacker: {attacker['name']}")
        state["log"].info(f"\t\tDefender: {defender['name']}")
        state["log"].info(f"\t\tHighest Roll for Hit: {hit_threshold}")
        state["log"].info(f"\t\tDie Roll: {die_roll}")

        if die_roll <= hit_threshold or die_roll == 1:
            state["log"].info("\t\tHit!")
            Unit.hurt(state, attacker_id, defender_id)
            if defender_id not in state["units"]:
                return defender_id
        else:
            state["log"].info("\t\t(Miss)")
        state["log"].info("")

    @staticmethod
    def destroy_non_combat_units(state: dict, pos: tuple):
        for unit in Board.get_units(state, pos):
            if unit["type"] in ("Decoy", "ColonyShip"):
                Unit.destroy(state, Unit.get_id(unit))

    @staticmethod
    def order(state: dict, pos: tuple):
        return [Unit.get_id(x) for x in sorted(Board.get_units(state, pos),
                key = lambda unit: (
                    from_type(unit["type"]).attack_class or 'Z',
                    unit["last_turn_moved"],
                    unit["num"]
                )
            )
            if x["type"] != "Homeworld"
        ]

    # Should move this to State module
    @staticmethod
    def generate_combat_state(state: dict) -> dict:
        return {
            pos: [
                {
                    "player": unit["player_id"],
                    "type": unit["type"],
                    "num": unit["num"],
                    "hits_left": from_type(unit["type"]).armor - unit["armor"],
                    "technology": Technology.copy_unit_tech(state, Unit.get_id(unit))
                } for unit in Unit.ids_to_units(state, CombatEngine.order(state, pos))
            ] for pos in Board.get_combat_positions(state)
        }
