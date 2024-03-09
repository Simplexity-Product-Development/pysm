from pysm import State, StateMachine, Event

class StateRoot(StateMachine):

    def __init__(self,name):
        super().__init__(name)
        self.enter_called = False

    def on_enter(self,state,event):
        self._log_event(event,"Entering")
        self.enter_called = True

    def on_exit(self,state,event):
        self._log_event(event,"Exiting")

    def on_tick(self,state,event):
        self._log_event(event,"Tick")

    def on_error(self,state,event):
        self._log_event(event,"Unhandled error event")

    def on_mystery(self,state,event):
        self._log_event(event,"Unhandled mystery event")

    def register_handlers(self):
        self.handlers = {
            "enter": self.on_enter,
            "exit": self.on_exit,
            "tick":self.on_tick,
            "error":self.on_error,
            "mystery":self.on_mystery,
        }

class StatePaused(State):

    def __init__(self,name):
        super().__init__(name)
        self.enter_called = False

    def on_enter(self,state,event):
        self._log_event(event, "Entering")
        self.enter_called = True

    def on_exit(self,state,event):
        self._log_event(event,"Exiting")

    def on_resume(self,state,event):
        self._log_event(event,"Resuming")

    def register_handlers(self):
        self.handlers = {
            "enter": self.on_enter,
            "exit": self.on_exit,
            "resume": self.on_resume,
        }

class StateWorking(StateMachine):

    def __init__(self,name):
        super().__init__(name)
        self.enter_called = False

    def on_enter(self,state,event):
        self._log_event(event,"Entering")
        self.enter_called = True

    def on_exit(self,state,event):
        self._log_event(event,"Exiting")

    def on_pause(self,state,event):
        self._log_event(event,"Pausing")

    def register_handlers(self):
        self.handlers = {
            "enter": self.on_enter,
            "exit": self.on_exit,
            "pause": self.on_pause,
        }

class Substate1(State):

    def __init__(self,name):
        super().__init__(name)
        self.enter_called = False

    def on_enter(self,state,event):
        self._log_event(event,"Entering")
        self.enter_called = True

    def on_exit(self,state,event):
        self._log_event(event,"Exiting")

    def on_step_complete(self,state,event):
        self._log_event(event,"Step Complete")

    def register_handlers(self):
        self.handlers = {
            "enter": self.on_enter,
            "exit": self.on_exit,
            "step_complete": self.on_step_complete,
        }

class Substate2(State):

    def __init__(self,name):
        super().__init__(name)
        self.enter_called = False

    def on_enter(self,state,event):
        self._log_event(event,"Entering")
        self.enter_called = True

    def on_exit(self,state,event):
        self._log_event(event,"Exiting")

    def on_step_complete(self,state,event):
        self._log_event(event,"Step Complete")

    def register_handlers(self):
        self.handlers = {
            "enter": self.on_enter,
            "exit": self.on_exit,
            "step_complete": self.on_step_complete,
        }

def test_substate_history():

    # States
    root = StateRoot("TopLevel")
    root.description = "Simple machine to substate history event."

    state_paused = StatePaused("Paused")
    root.add_state(state_paused)

    state_working = StateWorking("Working")
    root.add_state(state_working, initial=True)

    substate1 = Substate1("Substate1")
    state_working.add_state(substate1, initial=True )

    substate2 = Substate2("Substate2")
    state_working.add_state(substate2)

    # Transitions
    root.add_transition(state_working, state_paused,events=['pause'])
    root.add_transition(state_paused, state_working,events=['resume'])

    state_working.add_transition(substate1, substate2,events=['step_complete'])
    state_working.add_transition(substate2, substate1,events=['step_complete'])

    root.initialize()
    root.to_plantuml()

    # Verify initialize called on_enter for all states on path to initial leaf state.
    assert root.enter_called
    assert state_working.enter_called
    assert substate1.enter_called

    # Verify we start in correct state
    assert root.state == state_working
    assert root.leaf_state == substate1

    # Verify state path
    p = [root, state_working, substate1]
    assert root.state_path == p

    # Pause
    root.dispatch(Event("pause"))
    assert root.state == state_paused
    assert root.leaf_state == state_paused

    # Resume
    root.dispatch(Event("resume"))
    assert root.state == state_working
    assert root.leaf_state == substate1

    # Advance to second substate.
    root.dispatch(Event("step_complete"))
    assert root.state == state_working
    assert root.leaf_state == substate2

    # Pause
    root.dispatch(Event("pause"))
    assert root.state == state_paused
    assert root.leaf_state == state_paused

    # Resume
    root.dispatch(Event("resume"))
    assert root.state == state_working
    assert root.leaf_state == substate2 # "If this fails, the substate history is not working and we re-enter the initial state"

if __name__ == "__main__":
    test_substate_history()