# tests/enforcement/fixtures/allowed_init_only.py
class Engine:
    def __init__(self, cfg):
        self.cfg = cfg
        self.ready = True

    def process(self, x):
        return x * 2
