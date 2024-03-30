from test_simple_on_off import sm, state_on, state_off


def test_d2(complex_state_machine):

    sm = complex_state_machine
    sm.initialize()

    d2 = sm.to_d2()

    assert len(d2) > 0


def test_d2_with_tracking(complex_state_machine):

    sm = complex_state_machine
    sm.initialize()

    fn = f"HSM-{sm.name}-tracking.d2"
    d2 = sm.to_d2(show_visits=True, highlight_active=True, filename=fn)

    assert len(d2) > 0
