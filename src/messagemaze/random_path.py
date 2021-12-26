from .maze import Maze
from random import randint, shuffle
from typing import Tuple


def RandomPattern(size: Tuple[int, int], start: Tuple[int, int], end: Tuple[int, int], recur=0) -> Maze:
    """
    Return a random maze with the given size.
    """
    # Compute the distance between the start and end points
    dy = end[0] - start[0]
    dx = end[1] - start[1]

    # Number of addtional steps going right and down
    if recur < 3:
        var_x = randint(0, size[1]//3)
        var_y = randint(0, size[0]//3)
    else:
        var_x = 0
        var_y = 0

    # Compute the number of steps to take

    # Add the required steps to get to the end point
    steps = []
    if dx > 0:
        steps += [(1, 0)] * dx
    else:
        steps += [(-1, 0)] * -dx

    if dy > 0:
        steps += [(0, 1)] * dy
    else:
        steps += [(0, -1)] * -dy

    # Add the additional steps (variance in the path)
    steps += [(1, 0)] * var_x
    steps += [(-1, 0)] * var_x
    steps += [(0, 1)] * var_y
    steps += [(0, -1)] * var_y

    # Create a blank maze
    maze = Maze.Blank(*size)
    maze.set_start(*start)
    maze.set_end(*end)

    shuffle(steps)
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
            return RandomPattern(size, start, end, recur+1)

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
