import pygame
import sys
from simulator.sim import Simulator
from lib.keyboard import keyboard_event
from lib.utils import apply_coordinate, input_reader, coord_queue
import queue
import threading

# create pygame window
pygame.init()

WIDTH = 800
HEIGHT = 800
NODE_SIZE = 80  
state = {"fps": 5} 

#Color  (Red, Green, Blue) 0-2555
BLACK = (0, 0, 0)
DARK_GREY = (64, 64, 64)
MEDIUM_GREY = (128, 128, 128)
LIGHT_GREY = (192, 192, 192)
WHITE = (255, 255, 255)

# origin (0, 0) top left corner. x increase right, y increase down
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock() 
simulation = Simulator(WIDTH, HEIGHT, NODE_SIZE)
# second thread to read coord inputs in terminal while pygame is active 
threading.Thread(target=input_reader, daemon=True).start()


# Sim loop
def main():
    while True:
        # event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos() #tuple of the cursor x/y coordinates
                row = pos[1] // NODE_SIZE # index cell from px
                column = pos[0] // NODE_SIZE
                simulation.toggle_cell(row, column)

            elif event.type == pygame.KEYDOWN:
                # handles keyboard inputs from keyboard.py
                keyboard_event(simulation, event.key, state)

            # thread reads user inputs from terminal 
            while not coord_queue.empty():
                text = coord_queue.get()
                if apply_coordinate(simulation, text):
                    print(f"Applied coordinate from input: {text}")
                else:
                    pass

        # update simulation state
        simulation.update()
        # draw to window
        window.fill(DARK_GREY)
        simulation.draw(window)

        pygame.display.update()
        clock.tick(state["fps"])

if __name__ == "__main__":
    main()