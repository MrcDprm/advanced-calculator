from storage import load_json, save_json

MAX_ENTRIES = 100


class History:
    def __init__(self, file_name=None):
        self._file_name = file_name
        self._entries = []
        if file_name:
            data = load_json(file_name, [])
            if isinstance(data, list):
                self._entries = [tuple(entry) for entry in data
                                 if isinstance(entry, list) and len(entry) == 2
                                 and all(isinstance(item, str) for item in entry)]

    def add(self, expression, result):
        self._entries.append((expression, result))
        self._entries = self._entries[-MAX_ENTRIES:]
        self._save()

    def get_all(self):
        return list(self._entries)

    def clear(self):
        self._entries.clear()
        self._save()

    def is_empty(self):
        return len(self._entries) == 0

    def _save(self):
        if self._file_name:
            save_json(self._file_name, self._entries)
