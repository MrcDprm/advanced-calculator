import json
from pathlib import Path

DATA_DIR = Path.home() / ".advanced-calculator"


def load_json(name, default):
    try:
        with open(DATA_DIR / name, encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return default


def save_json(name, data):
    try:
        DATA_DIR.mkdir(exist_ok=True)
        with open(DATA_DIR / name, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError:
        pass
