# tests/test_input_parser.py

from pavepath.input_parser import parse_input   # ✅ correct


def test_parse_coordinates():
    result = parse_input([(33.8121, -117.9190)])
    assert result == [(33.8121, -117.9190)]

def test_parse_address():
    result = parse_input(["123 Main St, Menifee, CA"])
    assert result == [(33.8148, -117.9190)]  # Simulated

def test_parse_grid_id():
    result = parse_input(["B3"])
    assert result == [(33.7000, -117.9000)]  # Simulated

def test_invalid_input():
    try:
        parse_input(["invalid"])
        assert False
    except ValueError:
        assert True
