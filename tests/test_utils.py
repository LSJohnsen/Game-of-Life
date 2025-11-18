import pytest
from lib.utils import set_coordinate, apply_coordinate


# test functions for applying coordinates to sim 
def test_set_coordinate_valid_basic():
    # row col 10
    assert set_coordinate("a1b1", 10, 10) == (0, 0)
    assert set_coordinate("a3b5", 10, 10) == (2, 4)   
    assert set_coordinate("A2B4", 10, 10) == (1, 3)   # uppercase
    assert set_coordinate("  a10b1  ", 20, 20) == (9, 0)  # space


def test_set_coordinate_invalid_missing_row_or_col():
    assert set_coordinate("a1", 10, 10) is None     
    assert set_coordinate("b3", 10, 10) is None
    assert set_coordinate("garbage", 10, 10) is None

def test_set_coordinate_out_of_bounds():
    assert set_coordinate("a11b1", 10, 10) is None  # row too big
    assert set_coordinate("a1b11", 10, 10) is None  # col too big
    assert set_coordinate("a0b1", 10, 10) is None   # zero index should be one


class Grid:
    def __init__(self, rows, cols):
        self.cells = [[0 for _ in range(cols)] for _ in range(rows)]

class Sim:
    def __init__(self, rows, cols):
        self.rows = rows
        self.columns = cols
        self.grid = Grid(rows, cols)

def test_apply_coordinate_sets_cell_alive():
    sim = Sim(10, 10)
    assert apply_coordinate(sim, "a1b1") is True
    assert sim.grid.cells[0][0] == 1

def test_apply_coordinate_rejects_invalid():
    sim = Sim(5, 5)
    assert apply_coordinate(sim, "a6b1") is False   # bounds
    assert apply_coordinate(sim, "foo") is False    # invalid