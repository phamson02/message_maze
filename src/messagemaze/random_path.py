from .maze import Maze
from random import randint, shuffle
from typing import Tuple

def generate_random_steps(start: Tuple[int, int], end: Tuple[int, int], max_vars: Tuple[int, int]) -> list:
    """
    Generate random steps for the maze path between start and end points.

    Args:
        start (Tuple[int, int]): The starting position in the maze (row, column).
        end (Tuple[int, int]): The end position in the maze (row, column).
        max_vars (Tuple[int, int]): The maximum allowed additional steps in x and y directions.
        
    Returns:
        list: A shuffled list of steps.
    """
    dx, dy = end[1] - start[1], end[0] - start[0]
    var_x, var_y = randint(0, max_vars[0]), randint(0, max_vars[1])

    steps = [(1, 0) if dx > 0 else (-1, 0)] * abs(dx) + \
            [(0, 1) if dy > 0 else (0, -1)] * abs(dy) + \
            [(1, 0)] * var_x + [(-1, 0)] * var_x + [(0, 1)] * var_y + [(0, -1)] * var_y

    shuffle(steps)
    return steps

def random_pattern(size: Tuple[int, int], start: Tuple[int, int], end: Tuple[int, int], retry_count: int = 0) -> Maze:
    """
    Generate a random maze with the given size, start, and end points.
    
    Args:
        size (Tuple[int, int]): The dimensions of the maze (rows, columns).
        start (Tuple[int, int]): The starting position in the maze (row, column).
        end (Tuple[int, int]): The end position in the maze (row, column).
        retry_count (int, optional): The number of retries so far. Defaults to 0.
        
    Returns:
        Maze: A randomly generated maze instance.
    """
    
    if retry_count < 3:
        steps = generate_random_steps(start, end, (size[1]//3, size[0]//3))
    else:
        steps = generate_random_steps(start, end, (0, 0))

    # Create a blank maze
    maze = Maze.Blank(*size)
    maze.set_start(*start)
    maze.set_end(*end)

    current_cell = maze.start
    maze.solution_path.append(current_cell)
    seq = []
    n_move = 0
    thred = len(steps)  # Stuck threshold

    while steps:

        # Check if finished early
        if current_cell == maze.end:
            break

        # Check if stuck
        n_move += 1
        seq.append(current_cell)
        if n_move > thred and len(set(seq[-thred:])) == 1:
            return random_pattern(size, start, end, retry_count+1)

        dx, dy = steps.pop(0)

        next_cell_coors = (current_cell.i + dy, current_cell.j + dx)
        go = False

        # Check if the next cell is valid
        if maze.is_valid_cell(*next_cell_coors):
            next_cell = maze.cell_at(*next_cell_coors)
            if next_cell not in maze.solution_path:
                go = True
                current_cell.remove_walls(next_cell)
                current_cell = next_cell
                maze.solution_path.append(current_cell)

        # If the next cell is not valid, go back
        if not go:
            steps.append((dx, dy))

    return maze
