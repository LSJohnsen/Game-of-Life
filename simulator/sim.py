from simulator.board import Board
from lib.utils import if_stopped
from lib.rules import gol_step
from IO.IO import save_txt, load_txt, load_snapshot_csv, save_snapshot_csv, choose_snapshot_interactive
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]  
PATTERNS_DIR = BASE_DIR / "patterns"
SAVE_PATH = PATTERNS_DIR / "current.gol"
SAVE_PATH_SNAP = PATTERNS_DIR / "snap.txt"

# creates the gol simulation 
class Simulator:
    def __init__(self, width, height, node_size):
        self.grid = Board(width, height, node_size)
        self.temp_grid = Board(width, height, node_size)
        self.rows = height // node_size
        self.columns = width // node_size
        self.grid.fill_random()
        self.run = False

    def draw(self, window):
        self.grid.draw(window)


    def update(self):
        if self.is_running():
            gol_step(self.grid, self.temp_grid, self.rows, self.columns)
           
            for r in range(self.rows):
                for c in range(self.columns):
                    self.grid.cells[r][c] = self.temp_grid.cells[r][c]

    # is_running -> if_stopped -> running == false = true     
    def is_running(self):
        return self.run
    
    def start(self):
        self.run = True

    def stop(self):
        self.run = False

    @if_stopped
    def clear(self):
        self.grid.clear()
    
    @if_stopped
    def create_random_state(self):
        self.grid.fill_random()

    @if_stopped
    def toggle_cell(self, row, column):
        self.grid.toggle_cell(row, column)

    @if_stopped
    def single_step(self):
            was_running = self.run
            self.run = True
            self.update()
            self.run = was_running

    @if_stopped
    def save(self, path):
        save_txt(self.grid.cells, path)


    @if_stopped
    def load(self, path, mode="fit"):
        loaded, lr, lc = load_txt(path)
        # mode: "fit" = place into top-left, crop if larger
        #       "center" = center inside current grid
        #       "resize" = rebuild grid to loaded size
        if mode == "resize":
            self.grid.cells = [[0 for _ in range(lc)] for _ in range(lr)]
            self.temp_grid.cells = [[0 for _ in range(lc)] for _ in range(lr)]
            self.rows, self.columns = lr, lc

        # determine placement box
        R, C = self.rows, self.columns
        if mode == "center":
            r0 = max((R - lr) // 2, 0); c0 = max((C - lc) // 2, 0)
        else:  # "fit"
            r0 = 0; c0 = 0

        # clear and copy with cropping as needed
        for r in range(self.rows):
            for c in range(self.columns):
                self.grid.cells[r][c] = 0
        for r in range(min(lr, self.rows)):
            for c in range(min(lc, self.columns)):
                self.grid.cells[r + r0 if mode=="center" else r][c + c0 if mode=="center" else c] = loaded[r][c]

    @if_stopped
    def log_snapshot(self, path="runs/history.csv"):
        save_snapshot_csv(self.grid.cells, path)

    @if_stopped
    def load_snapshot(self, index, path="runs/history.csv"):
        cells = load_snapshot_csv(index, self.rows, self.columns, path)
        for r in range(self.rows):
            for c in range(self.columns):
                self.grid.cells[r][c] = cells[r][c]