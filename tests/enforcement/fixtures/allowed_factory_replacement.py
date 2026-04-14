# tests/enforcement/fixtures/allowed_factory_replacement.py
class Engine:
    def __init__(self, state):
        self.state = state

    def with_state(self, state):
        return Engine(state)  # ✅ replace, don’t mutate
