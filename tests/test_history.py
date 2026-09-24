import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import storage
from history import MAX_ENTRIES, History


class TestHistory(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.patcher = patch.object(storage, "DATA_DIR", Path(self.temp_dir.name))
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.temp_dir.cleanup()

    def test_add_and_clear(self):
        history = History()
        self.assertTrue(history.is_empty())
        history.add("2+2", "4")
        self.assertEqual(history.get_all(), [("2+2", "4")])
        history.clear()
        self.assertTrue(history.is_empty())

    def test_keeps_only_last_entries(self):
        history = History()
        for number in range(MAX_ENTRIES + 5):
            history.add(str(number), str(number))
        entries = history.get_all()
        self.assertEqual(len(entries), MAX_ENTRIES)
        self.assertEqual(entries[0], ("5", "5"))

    def test_get_all_returns_copy(self):
        history = History()
        history.add("1+1", "2")
        history.get_all().clear()
        self.assertFalse(history.is_empty())

    def test_saves_and_loads_from_file(self):
        History("history.json").add("3*3", "9")
        self.assertEqual(History("history.json").get_all(), [("3*3", "9")])

    def test_corrupt_file_starts_empty(self):
        (Path(self.temp_dir.name) / "history.json").write_text("bozuk", encoding="utf-8")
        self.assertTrue(History("history.json").is_empty())
