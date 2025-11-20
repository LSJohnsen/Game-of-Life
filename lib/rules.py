
"""
Contains simulation rules used in sim.py 
"""

# Check if surrounding nodes are alive 
def neighbors_alive(grid, row, column, rows, cols):
        """
        around each neighbor for ex:
         alive: [5,5]  (0,0)
            above: [4,5] (-1,0)
            below: [6,5] (1,0)
            left: [5,4] (0,-1)
            right: [5,6] (0,1)
            diagonal up left: [4,4] (-1,-1)
            diagonal up right: [4,6] (-1,1)
            diagonal down left: [6,5] (1,-1)
            diagonal down right: [6,6] (1,1)
        """

        live_neighbors = 0
        neighbors = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)] # index around each node

        # loop over the possible locations around each node and mark if neighbor is alive
        for nodes in neighbors:  
            new_r = (row+nodes[0]) % rows
            new_c = (column+nodes[1]) % cols 
            # modulo to wrap around edges so top and bottom are neighbors etc

            if grid.cells[new_r][new_c] == 1:
                live_neighbors += 1
        return live_neighbors

# computes one step following conway game of life rules and updates the grid 
def gol_step(grid, temp_grid, rows, cols):
    for r in range(rows):
        for c in range(cols):
            n = neighbors_alive(grid, r, c, rows, cols)  # rows, cols in correct order
            cell = grid.cells[r][c]
            if cell == 1:
                temp_grid.cells[r][c] = 1 if n in (2, 3) else 0
            else:
                temp_grid.cells[r][c] = 1 if n == 3 else 0