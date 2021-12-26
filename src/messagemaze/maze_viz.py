import pygame


class Visualizer:

    def __init__(self, maze, screen_size=(600, 400)):

        pygame.init()

        self.maze = maze
        self.n = maze.n
        self.m = maze.m

        self.screen = pygame.display.set_mode(screen_size)
        self.screen.fill('white')
        self.cell_size = self._cell_size()
        self.thick = 2
        self.clock = pygame.time.Clock()

        self.surface = pygame.Surface(self._surface_size())

    def _cell_size(self):
        '''Return the side length of a square on screen'''
        w = min(self.screen.get_height()//self.n,
                self.screen.get_width()//self.m)
        return w

    def _surface_size(self):
        '''Return the size of the surface'''
        w = self.cell_size
        return (self.m * w + self.thick, self.n * w + self.thick)

    def _draw(self, show_solution=False, show_visited=False, show_frontier=False):
        '''Draw the maze on screen'''
        w = self.cell_size

        if show_solution:
            for cell in self.maze.solution_path:
                y = cell.i * w
                x = cell.j * w
                pygame.draw.rect(self.surface, 'Red', (x, y, w, w))

        if show_visited:
            for row in self.maze.cells:
                for cell in row:
                    if cell.visited:
                        y = cell.i * w
                        x = cell.j * w
                        pygame.draw.rect(
                            self.surface, (69, 139, 0), (x, y, w, w))

        if show_frontier:
            for cell in self.maze.frontier:
                y = cell.i * w
                x = cell.j * w
                pygame.draw.rect(self.surface, 'Green', (x, y, w, w))

        for row in self.maze.cells:
            for cell in row:
                y = cell.i * w
                x = cell.j * w
                if cell.walls['N']:
                    pygame.draw.line(self.surface, 'Black',
                                     (x, y), (x+w, y), self.thick)
                if cell.walls['E']:
                    pygame.draw.line(self.surface, 'Black',
                                     (x+w, y), (x+w, y+w), self.thick)
                if cell.walls['S']:
                    pygame.draw.line(self.surface, 'Black',
                                     (x+w, y+w), (x, y+w), self.thick)
                if cell.walls['W']:
                    pygame.draw.line(self.surface, 'Black',
                                     (x, y+w), (x, y), self.thick)

    def show_maze(self, show_solution=False):
        '''Show the maze on screen'''

        surface_rect = self.surface.get_rect(
            center=self.screen.get_rect().center)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.surface.fill('white')
            self._draw(show_solution)
            self.screen.blit(self.surface, surface_rect)

            pygame.display.update()

    def save_fig(self, filename, show_solution=False):
        '''Save the maze'''

        canvas = pygame.Surface(
            (self.surface.get_width() + 50, self.surface.get_height() + 50))

        surface_rect = self.surface.get_rect(center=canvas.get_rect().center)

        canvas.fill('white')
        self.surface.fill('white')
        self._draw(show_solution)
        canvas.blit(self.surface, surface_rect)
        pygame.image.save(canvas, f'{filename}.png')
        pygame.quit()

    def visualize_generation(self, algorithm, *args):
        '''Show the process of maze generartion algorithm on screen'''
        from .visualize_algorithms import rBFS, BFS, DFS

        if algorithm == 'rBFS':
            algo = rBFS
        elif algorithm == 'BFS':
            algo = BFS
        elif algorithm == 'DFS':
            algo = DFS
        else:
            raise ValueError('Invalid algorithm')

        surface_rect = self.surface.get_rect(
            center=self.screen.get_rect().center)

        gen = algo(self.maze, *args)
        notify = False
        has_more = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.surface.fill('white')

            if has_more:
                maze, has_more = next(gen)
                self.maze = maze
            elif not notify:
                print('Finished')
                notify = True
            self._draw(show_visited=True, show_frontier=True)

            self.screen.blit(self.surface, surface_rect)

            pygame.display.update()
            self.clock.tick(30)
