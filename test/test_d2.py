from test_simple_on_off import sm, state_on, state_off


def test_d2(complex_state_machine):

    sm = complex_state_machine
    sm.initialize()

    d2 = sm.to_d2(show_visits=True)

    assert len(d2) > 0
