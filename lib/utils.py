
from functools import wraps
import numpy as np
import pygame
import re
import threading
import queue


#  bool checks in sim 
def if_stopped(func):       
    @wraps(func)
    def wrapper(self, *args, **kwargs): 
        if self.is_running():           # return if sim is running
            return
        return func(self, *args, **kwargs) #run function if sim not 
    return wrapper

#https://www.w3schools.com/python/python_regex.asp
    # \d = [0, 9]

def set_coordinate(input, total_rows, total_columns):

    # get coord as (a(num)b(num))
    reg = r"(a\d+|b\d+)"
    inputs = re.findall(reg, input.lower())

    row, column = None, None

    for i in inputs:
        letter = i[0] 
        num = int(i[1:])-1 # set back to zero index
    
        if letter == "a":
            row = num
        if letter == "b":
            column = num

    # need both row and column
    if row is None or column is None:
        return None

    # check bounds
    if row < 0 or row >= total_rows or column < 0 or column >= total_columns:
        return None

    return row, column

def apply_coordinate(sim, input):
    running = True

    coords = set_coordinate(input, sim.rows, sim.columns)
    if coords is None: 
        print(f"Invalid coordinate: {input}, must be a(num)b(num) within (a{sim.rows}b{sim.columns})")
        return False
    
    row, column = coords
    sim.grid.cells[row][column] = 1
    return True



# Read input
coord_queue = queue.Queue()
def input_reader():
    while True:
        try:
            coord = input("coord (a(num)b(num)), empty to ignore): ")
        except:
            print("input closed.")
            break
        coord = coord.strip()
        if not coord:
            continue

        coord_queue.put(coord)