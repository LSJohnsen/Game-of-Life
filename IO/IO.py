from pathlib import Path
import csv
import numpy as np

def save_txt(cells, path):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w") as f:
        for row in cells:
            f.write("".join(str(int(v)) for v in row) + "\n")

def load_txt(path):
    p = Path(path)
    with p.open("r") as f:
        lines = [line.rstrip("\n") for line in f]
    rows = len(lines)
    cols = len(lines[0]) if rows else 0
    cells = [[1 if ch == "1" else 0 for ch in line] for line in lines]
    return cells, rows, cols


def save_snapshot_csv(nodes, path="runs/history.csv"): #append a 1d array to a csv file with the saved state
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    flat = [int(v) for row in nodes for v in row] # flatten 2d to 1d array
    with p.open("a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(flat)

# reshape logic from VRX WAMV git repo mapping IO
def load_snapshot_csv(index, rows, cols, path="runs/history.csv"):
    with open(path, newline="") as f:
        reader = list(csv.reader(f))
    flat = np.array(reader[index], dtype=int)
    return flat.reshape((rows, cols)) #back to 2d

def choose_snapshot_interactive(sim, csv_path="runs/history.csv", preview_path="patterns/preview.gol"):
    p = Path(csv_path)
    if not p.exists():
        print(f"No history file: {csv_path}")
        return

    with p.open(newline="") as f:
        rows = list(csv.reader(f))

    total = len(rows)
    if total == 0:
        print("No snapshots found.")
        return

    print(f"{total-1} snapshots available (0-{total-1})")

    while True:
        try:
            index = int(input("Enter snapshot number to load: ").strip())
            if 0 <= index < total:
                break
            else:
                print("Snapshot number does not exist. Try again.")
        except ValueError:
            print("Invalid number. Try again.")

    flat = np.array(rows[index], dtype=int)
    cells = flat.reshape((sim.rows, sim.columns)).tolist()

    # valid yes no
    while True:
        save_ans = input("Save this snapshot to a preview file first? (y/n): ").strip().lower()
        if save_ans in ("y", "n"):
            break
        print("Invalid option. Enter y or n.")

    if save_ans == "y":
        Path(preview_path).parent.mkdir(parents=True, exist_ok=True)
        save_txt(cells, preview_path)
        print(f"Preview saved to {preview_path}")

    while True:
        apply_ans = input("Apply this snapshot to the simulator now? (y/n): ").strip().lower()
        if apply_ans in ("y", "n"):
            break
        print("Invalid option. Enter y or n.")

    if apply_ans == "y":
        for r in range(sim.rows):
            for c in range(sim.columns):
                sim.grid.cells[r][c] = cells[r][c]
        print(f"Applied snapshot {index} to simulator.")