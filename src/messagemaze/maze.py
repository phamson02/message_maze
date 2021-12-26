from .cell import Cell
from .maze_viz import Visualizer
import pickle
import os


class Maze:
    '''
    Class represing a maze.

    Attributes:
    -----------
    n : int
        number of rows
    m : int
        number of columns
    shape : tuple
        (n, m)
    template : list of lists
        a list of lists of Cell objects
    start : Cell
        the starting cell
    end : Cell
        the ending cell
    solution_path : list of Cell
        the solution path
    '''

    def __init__(self, n, m, template=None, start=None, end=None, solution_path=None):
        '''Create a Maze object of size n, m'''
        self.n = n
        self.m = m
        self.shape = (n, m)
        self.cells = template
        self.start = start
        self.end = end
        self.solution_path = solution_path or []
        self.generated = False
        self.frontier = []

    @classmethod
    def Blank(cls, n, m):
        '''Create a blank (full-of-wall) Maze object of size n, m'''
        blank = [[Cell(i, j) for j in range(m)] for i in range(n)]
        return cls(n, m, blank)

    @classmethod
    def from_file(cls, filename):
        '''Create a Maze object from a file in subfolder "patterns"'''
        import importlib.resources
        from . import patterns
        pattern = pickle.load(
            importlib.resources.open_binary(patterns, f'{filename}.pickle')
        )
        return cls(pattern.n, pattern.m, pattern.cells, pattern.start, pattern.end, pattern.solution_path)

    def to_file(self, filename):
        '''Save the maze to a file in subfolder "patterns"'''
        data_dir = os.path.join(os.path.dirname(__file__), 'patterns')
        data_path = os.path.join(data_dir, f'{filename}.pickle')
        with open(data_path, 'wb') as f:
            pickle.dump(self, f)

    def set_start(self, i, j):
        '''Set the starting cell of the maze'''
        self.start = self.cells[i][j]

    def set_end(self, i, j):
        '''Set the ending cell of the maze'''
        self.end = self.cells[i][j]

    def start_cell(self):
        '''Return the starting cell'''
        return self.start

    def end_cell(self):
        '''Return the ending cell'''
        return self.end

    def get_cells(self):
        return self.cells

    def set_cells(self, cells):
        self.cells = cells

    def cell_at(self, i, j):
        '''Return the cell at position i, j'''
        return self.cells[i][j]

    def is_valid_cell(self, i, j) -> bool:
        '''Check if there exists a cell with given indexes in the maze'''
        return 0 <= i < self.shape[0] and 0 <= j < self.shape[1]

    def get_neighbours(self, cell):
        '''Return the neighbours of a cell'''
        neighbours = []
        if cell.i > 0:
            neighbours.append(self.cells[cell.i-1][cell.j])
        if cell.i < self.shape[0]-1:
            neighbours.append(self.cells[cell.i+1][cell.j])
        if cell.j > 0:
            neighbours.append(self.cells[cell.i][cell.j-1])
        if cell.j < self.shape[1]-1:
            neighbours.append(self.cells[cell.i][cell.j+1])
        return neighbours

    def _set_door(self, cell):
        if cell.j == 0:
            cell.walls['W'] = False
        elif cell.j == self.shape[1]-1:
            cell.walls['E'] = False
        elif cell.i == 0:
            cell.walls['N'] = False
        elif cell.i == self.shape[0]-1:
            cell.walls['S'] = False

    def generate_maze(self, algorithm='rBFS', *args):
        '''Generate the maze using the specified algorithm'''
        if self.generated:
            print('Maze already generated')
            return

        from .algorithms import rBFS, BFS, DFS
        if not self.start:
            self.start = self.cells[0][0]
        if not self.end:
            self.end = self.cells[-1][-1]

        if algorithm == 'rBFS':
            rBFS(self, *args)
        elif algorithm == 'BFS':
            BFS(self)
        elif algorithm == 'DFS':
            DFS(self)
        else:
            raise ValueError('Invalid algorithm')

        self._set_door(self.start)
        self._set_door(self.end)
        self.generated = True

    def show_maze(self, show_solution=False):
        '''Visualize the maze'''
        Visualizer(self).show_maze(show_solution)

    def save_fig(self, filename, show_solution=False):
        '''Save the maze to a file'''
        Visualizer(self).save_fig(filename, show_solution)
