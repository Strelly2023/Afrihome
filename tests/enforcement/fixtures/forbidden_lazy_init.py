# tests/enforcement/fixtures/forbidden_lazy_init.py
class CacheUser:
    def __init__(self):
        self.cache = None

    def load(self, k):
        if self.cache is None:
            self.cache = {}  # ❌ forbidden
        return self.cache.get(k)
