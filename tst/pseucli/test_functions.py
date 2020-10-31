from pseucli import parse_dice, parse_range, Range, CliError
import pytest

def test_parse_dice():
    pass_cases = [
        ("1d6", Range(1, 1, 6)),
        ("2d2", Range(2, 1, 2)),
        ("1d1", Range(1, 1, 1))
    ]
    fail_cases = [
        "d",
        "1d",
        "d1",
        "0d6",
        "1d0"
    ]
    for s, expected in pass_cases:
        assert expected == parse_dice(s)
    for s in fail_cases:
        with pytest.raises(CliError):
            parse_dice(s)

def test_parse_range():
    pass_cases = [
        ("1", Range(1, 0, 0)),
        ("2", Range(1, 0, 1)),
        ("0-4", Range(1, 0, 4)),
        ("1-4x3", Range(3, 1, 4))
    ]
    fail_cases = [
        "0",
        "-1",
        "-1-0",
        "1-4x0",
        "1-0"
    ]
    for s, expected in pass_cases:
        assert expected == parse_range(s)
    for s in fail_cases:
        with pytest.raises(CliError):
            parse_range(s)
