import sys
sys.path.append(r'.')

import pysm

def test_d2():
    # Define general state machine for test
    sm1 = pysm.StateMachine("sm1")

    # Put a generic state in the SM
    state1 = pysm.State("state1")
    sm1.add_state(state1, initial=True)
    
    # Create a child SM
    sm2 = pysm.StateMachine("sm2")
    sm1.add_state(sm2)
    sm1.add_transition(state1, sm2, events=["evt_state1->sm2"])

    # Add a transition for the child SM that returns to itself
    sm1.add_transition(sm2, None, events=["evt_sm2->sm2"])

    # Add a transition for the child SM that returns to itself
    def dummy_action(event, state):
        pass
    sm1.add_transition(sm2, None, events=["evt_sm2->sm2_func"], action=dummy_action)

    # Create initial landing state for child SM
    state2 = pysm.State("state2")
    sm2.add_state(state2, initial=True)

    # Add self-transition for this state
    sm2.add_transition(state2, None, events=["evt_state2->state2"])

    # Make new child state with other forms of transitions
    state3 = pysm.State("state3")
    sm2.add_state(state3)
    sm2.add_transition(state2, state3, events=["evt_state2->state3_func"], action=dummy_action)
    sm2.add_transition(state3, state2, events=["evt_state3->state2_func"], action=dummy_action)
    sm2.add_transition(state3, state3, events=["evt_state3->state3_func"], action=dummy_action)
    
    # Intialise SM
    sm1.initialize()

    # Run tool to generate D2 graph
    d2 = sm1.to_d2()

    # Verify that the D2 graph is not empty.
    assert len(d2) > 0

    # You can also check the output file: HSM-sm1.d2

if __name__ == '__main__':
    test_d2()