from functools import wraps
from IO.IO import choose_snapshot_interactive
import pygame
from lib.utils import apply_coordinate

# Dictionary storing keyboard inputs
keys = {}

'''
decorator to store keyboard inputs and handle event. 
saves any applied key to a dictionary, where the keyboard_event gets called in case of pressing the corresponding key,
where this gets parsed to the simulator
'''
# stores which function shoud be used for each key in dictionary
def keyboard_in(key):         
    def decorator(func):
        keys[key] = func            # ex. keys[pygame.K_return] = start_sim
        return func
    return decorator

# looks up stored keys and runs the function stored with it 
def keyboard_event(simulation, key, state=None):
    handler = keys.get(key)         # ex. press K -> handler = start_sim
    if handler:
        handler(simulation, state)  # start_sim(simulation, state)

# Keyboard functions (handling of fps state error fixed by gpt)

@keyboard_in(pygame.K_RETURN)
def start_sim(sim, state):
    sim.start()
    pygame.display.set_caption("Simulation is running")

@keyboard_in(pygame.K_SPACE)
def stop_sim(sim, state):
    sim.stop()
    pygame.display.set_caption("Simulation is stopped")

@keyboard_in(pygame.K_r)
def random_state(sim, state):
    sim.create_random_state()

@keyboard_in(pygame.K_c)
def clear_sim(sim, state):
    sim.clear()

@keyboard_in(pygame.K_f)
def fps_up(sim, state):
    # state dict provided from main
    if state is not None:
        state["fps"] = min(state.get("fps", 0) + 2, 120)

@keyboard_in(pygame.K_s)
def fps_down(sim, state):
    if state is not None:
        state["fps"] = max(state.get("fps", 0) - 2, 1)

@keyboard_in(pygame.K_UP)
def single_step(sim, state):
    sim.single_step()

@keyboard_in(pygame.K_p) 
def save_pattern(sim, state):
    sim.save("patterns/current.gol")

@keyboard_in(pygame.K_l)  
def load_pattern(sim, state):
    sim.load("patterns/current.gol", mode="center")   

@keyboard_in(pygame.K_u)
def log_snapshot(sim, state):
    sim.log_snapshot()
    pygame.display.set_caption("Snapshot logged")

@keyboard_in(pygame.K_i)
def load_snapshot(sim, state):
    choose_snapshot_interactive(sim)
    pygame.display.set_caption("Loaded chosen snapshot")


# @keyboard_in(pygame.K_t)
# def write_coordinates(sim, state):
    
#     print("Enter coordinate in terminal (example: a1b1). Leave empty to cancel.")
    
#     line = input(f"enter the coordinates to set node to living (e.g. a1b1): ").strip()

#     if not line:
#         print("No coordinate entered, cancelled.")
#         return

#     if not apply_coordinate(sim, line):
#         print("Invalid input. Must be a(num)b(num), e.g. a3b5.")
#     else:
#         print(f"Applied coordinate: {line}")

#     pygame.display.set_caption("Coordinates applied")

'''
BASE_DIR = Path(__file__).resolve().parents[1]  
PATTERNS_DIR = BASE_DIR / "patterns"
SAVE_PATH = PATTERNS_DIR / "current.gol"
SAVE_PATH_SNAP = PATTERNS_DIR / "snap.txt"
'''
