# tests/enforcement/fixtures/forbidden_post_init.py
class Service:
    def __init__(self):
        self.ready = False

    def start(self):
        self.ready = True   #