import sys
sys.path.append("src")
from economic_engine import EconomicEngine
from initial_state import initial_state as state1
from final_state import final_state as state2
from state import State
from strategies import Strategy1, Strategy2

state = State.from_standard(state1, [Strategy1, Strategy2])
EconomicEngine.run_phase(state)
state2 = State.from_standard(state2, [Strategy1, Strategy2])

assert State.compare_native_states(state, state2)

print("This test passed: Economic Phase 1")
