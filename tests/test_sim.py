from simulator.sim import Simulator

# Test simulator rules

def make_empty_sim(rows=10, cols=10):
    
    sim = Simulator(width=cols, height=rows, node_size=1)
    for r in range(rows):
        for c in range(cols):
            sim.grid.cells[r][c] = 0
    return sim

def test_underpopulation():
    sim = make_empty_sim(5, 5)
    sim.grid.cells[2][2] = 1
    sim.start()              
    sim.update()
    assert sim.grid.cells[2][2] == 0

def test_reproduction():
    sim = make_empty_sim(10, 10)
    sim.grid.cells[1][1] = 1
    sim.grid.cells[1][2] = 1
    sim.grid.cells[2][1] = 1   # three neighbors around (2,2)
    sim.start()
    sim.update()
    assert sim.grid.cells[2][2] == 1   # dead cell becomes alive