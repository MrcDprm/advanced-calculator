class History:
    def __init__(self):
        self._entries = []


    def add(self, expression, result):
        self._entries.append((expression, result))

    def get_all(self):
        return list(self._entries)

    def clear(self):
        self._entries.clear()

    def is_empty(self):
        return len(self._entries) == 0

    