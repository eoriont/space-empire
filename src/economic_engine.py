class EconomicEngine:
    @staticmethod
    def run_phase(state: dict):
        turn = state["turn"]
        state["phase"] = "Economic"
        # state["log"].info(f"BEGINNING OF TURN {turn} ECONOMIC PHASE\n")
