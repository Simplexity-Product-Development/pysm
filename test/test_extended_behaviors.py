from pysm import State, Event


def test_states_all(complex_state_machine):

    sm = complex_state_machine
    sm.initialize()

    states = sm.states_all

    print(states)

    assert (
        len(states) == 4
    )  # Paused, Working, Working.Substate1, Working.Substate2


def test_get_state(complex_state_machine):

    sm = complex_state_machine

    # Add in a test state
    name = "TestState"
    test_state = State(name)
    sm.add_state(test_state)

    sm.initialize()

    state = sm.state_get_by_name(name)

    assert test_state == state

    assert state.name == name


def test_visit_counting(complex_state_machine):
    sm = complex_state_machine
    sm.initialize()

    # Upon init, should have updated visit counts.
    state_working = sm.state_get_by_name("Working")
    assert state_working.visits == 1
    assert state_working.visited

    state_substate1 = sm.state_get_by_name("Substate1")
    assert state_substate1.visits == 1
    assert state_substate1.visited

    state_substate2 = sm.state_get_by_name("Substate2")
    assert state_substate2.visits == 0
    assert not state_substate2.visited

    state_paused = sm.state_get_by_name("Paused")
    assert state_paused.visits == 0
    assert not state_paused.visited

    # Force a transition and recheck state visit counts
    sm.dispatch(Event("step_complete"))

    state_working = sm.state_get_by_name("Working")
    assert state_working.visits == 1

    state_substate1 = sm.state_get_by_name("Substate1")
    assert state_substate1.visits == 1

    state_substate2 = sm.state_get_by_name("Substate2")
    assert state_substate2.visits == 1

    state_paused = sm.state_get_by_name("Paused")
    assert state_paused.visits == 0

    # Pause
    sm.dispatch(Event("pause"))

    state_working = sm.state_get_by_name("Working")
    assert state_working.visits == 1

    state_substate1 = sm.state_get_by_name("Substate1")
    assert state_substate1.visits == 1

    state_substate2 = sm.state_get_by_name("Substate2")
    assert state_substate2.visits == 1

    state_paused = sm.state_get_by_name("Paused")
    assert state_paused.visits == 1

    # Resume
    sm.dispatch(Event("resume"))
    assert sm.leaf_state == state_substate2

    state_working = sm.state_get_by_name("Working")
    assert state_working.visits == 2

    state_substate1 = sm.state_get_by_name("Substate1")
    assert state_substate1.visits == 1

    state_substate2 = sm.state_get_by_name("Substate2")
    assert state_substate2.visits == 2

    state_paused = sm.state_get_by_name("Paused")
    assert state_paused.visits == 1

    # Return to substate 1
    sm.dispatch(Event("step_complete"))
    assert sm.leaf_state == state_substate1

    state_working = sm.state_get_by_name("Working")
    assert state_working.visits == 2

    state_substate1 = sm.state_get_by_name("Substate1")
    assert state_substate1.visits == 2

    state_substate2 = sm.state_get_by_name("Substate2")
    assert state_substate2.visits == 2

    state_paused = sm.state_get_by_name("Paused")
    assert state_paused.visits == 1
