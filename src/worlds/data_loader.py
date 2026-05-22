from __future__ import annotations

import json
import os
from typing import Any


def _data_path(filename: str) -> str:
    # root/RPG/src/worlds/data_loader.py -> root/RPG/data
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, "..", ".."))
    return os.path.join(root, "data", filename)


def load_monsters() -> list[dict[str, Any]]:
    path = _data_path("monsters.json")
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

