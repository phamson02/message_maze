class Cell:
    '''
    Class representing a cell.

    Attributes:
    -----------
    i : int
        Row index of the cell.
    j : int
        Column index of the cell.
    walls : dict
        Dictionary of the status of walls of the cell.
    visited : bool
        Whether the cell has been visited or not.
    '''

    def __init__(self, i, j):
        '''Create a Cell object with indexes (i, j), four walls and marked unvisited'''
        self.i = i
        self.j = j
        self.walls = {'N': True, 'W': True, 'S': True, 'E': True}
        self.visited = False

    def remove_walls(self, other):
        '''Remove walls between two adjacent cells'''
        dx = self.j - other.j
        dy = self.i - other.i

        # Check if removing walls is possible
        if dx * dy != 0 or abs(dx + dy) != 1:
            return -1

        if dy == 1:
            self.walls['N'] = False
            other.walls['S'] = False
        elif dy == -1:
            self.walls['S'] = False
            other.walls['N'] = False

        if dx == 1:
            self.walls['W'] = False
            other.walls['E'] = False
        elif dx == -1:
            self.walls['E'] = False
            other.walls['W'] = False

    def add_walls(self, other):
        '''Adding walls between two adjacent cells'''
        dx = self.j - other.j
        dy = self.i - other.i

        # Check if adding walls is possible
        if dx * dy != 0 or abs(dx + dy) != 1:
            return -1

        if dy == 1:
            self.walls['N'] = True
            other.walls['S'] = True
        elif dy == -1:
            self.walls['S'] = True
            other.walls['N'] = True

        if dx == 1:
            self.walls['W'] = True
            other.walls['E'] = True
        elif dx == -1:
            self.walls['E'] = True
            other.walls['W'] = True

    def set_visited(self):
        '''Set a cell as visited'''
        self.visited = True

    def set_unvisited(self):
        '''Set a cell as unvisited'''
        self.visited = False

    def is_visited(self):
        '''Check if a cell is visited'''
        return self.visited
