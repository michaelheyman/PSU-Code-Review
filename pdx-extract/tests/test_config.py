import pytest

from app import config

levels = [("critical", 50), ("error", 40), ("warning", 30), ("info", 20), ("debug", 10)]


@pytest.mark.parametrize("level, expected", levels)
def test_type(level, expected):
    assert config.map_level(level) == expected


def test_map_level_returns_10_when_invalid():
    level = "invalid-level"

    mapped_level = config.map_level(level)

    assert mapped_level == 10
