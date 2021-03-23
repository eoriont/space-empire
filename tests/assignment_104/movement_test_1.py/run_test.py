import sys
sys.path.append("src")
from movement_engine import MovementEngine
from initial_state import game_state as state1
from final_state import game_state as state2
from state import State
from strategies import Strategy

state = State.from_standard(state1, [Strategy, Strategy])
MovementEngine.run_phase(state)
state2 = State.from_standard(state2, [Strategy, Strategy])

assert State.compare_native_states(state, state2)

print("This test passed: Movement Phase 1")
