# Game-of-Life

# Conway’s Game of Life

Contains an implementation of Conway’s Game of Life written in Python with Pygame.  
The program simulates the evolution of a two–dimensional grid of cells and provides both graphical and terminal based interaction for creating and inspecting patterns.

The code is structured into clear modules that separate simulation logic, rendering, input handling, file operations, and tests, making the project easier to understand, extend, and maintain.

---

## Features

- Interactive Game of Life simulation in a Pygame window
- Modular design:
  - `board` for grid representation and drawing
  - `rules` for update logic
  - `simulator` for running the simulation
  - utility modules for keyboard mapping, coordinate handling, and I/O
- Keyboard controls for starting, stopping, stepping, and modifying the simulation
- Terminal input thread for entering cell coordinates without blocking the GUI
- Saving and loading patterns from text files
- Snapshot logging and loading from CSV history
- Input validation using range checks and regular expressions
- Automated tests using `pytest` for core logic and utilities

---

## Project Structure

```text
GAME_OF_LIFE/
  IO/
    IO.py                 # File handling for patterns and snapshots
  lib/
    keyboard.py           # Keyboard decorator and event dispatch
    rules.py              # Game of Life update rules
    utils.py              # Coordinate parsing, threading helpers, etc.
  patterns/
    current.gol           # Saved pattern (example)
    preview.gol           # Preview pattern (example)
  runs/
    history.csv           # Snapshot history for simulator states
  simulator/
    board.py              # Board class: grid storage and drawing
    sim.py                # Simulator class: main simulation logic
  tests/
    test_sim.py           # Tests for simulator logic
    test_utils.py         # Tests for utilities (e.g. coordinate parsing)
  main.py                 # Entry point for running the simulation
