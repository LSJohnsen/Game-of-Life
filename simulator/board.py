import pygame
import random

# makes pygame board 
class Board:
    def __init__(self, width, height, node_size):
        self.rows = height // node_size
        self.columns = width // node_size
        self.node_size = node_size
        self.cells = [[0 for _ in range(self.columns)] for _ in range(self.rows)] #list of zeroes for columns in rows

    def draw(self, window):
        for row in range(self.rows):
            for column in range(self.columns):
                color = (255, 165, 0) if self.cells[row][column] else (55, 55, 55) #rgb
                pygame.draw.rect(window, color, (column * self.node_size, row * self.node_size, self.node_size - 1, self.node_size - 1)) # 1 pixel smaller for lines

    # randomly fill with living cells
    # This code was modified from AI - small change in randomizer logic not really needed 
    def fill_random(self):  
        for row in range(self.rows):
            for column in range(self.columns):
                self.cells[row][column] = int(random.random() < 0.25) 

    def clear(self):
        for row in range(self.rows):
            for column in range(self.columns):
                self.cells[row][column] = 0

    # check bounds and toggle
    def toggle_cell(self, row, column):
        if 0 <= row < self.rows and 0 <= column < self.columns:
            self.cells[row][column] = 1 - self.cells[row][column]
            