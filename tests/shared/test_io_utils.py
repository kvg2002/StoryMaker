import json
from pathlib import Path

from shared.io_utils import read_json, write_json


def test_write_json_creates_parent_dirs_and_file(tmp_path: Path) -> None:
    target = tmp_path / "nested" / "out.json"

    write_json({"a": 1}, target)

    assert target.exists()
    assert json.loads(target.read_text(encoding="utf-8")) == {"a": 1}


def test_read_json_round_trips_unicode(tmp_path: Path) -> None:
    target = tmp_path / "out.json"
    write_json({"caption": "이순신이 절뚝거리며 걸음"}, target)

    result = read_json(target)

    assert result["caption"] == "이순신이 절뚝거리며 걸음"
