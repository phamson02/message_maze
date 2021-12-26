from random import shuffle


def DFS(maze):
    cellStack = []
    maze.frontier = cellStack

    if not maze.solution_path:
        maze.start.set_visited()
        cellStack.append(maze.start)
    else:
        # push all the cells from the solution path to the stack
        for cell in maze.solution_path:
            cell.set_visited()
            cellStack.append(cell)

    currentCell = maze.start
    while cellStack:
        yield maze, True
        neighbours = maze.get_neighbours(currentCell)
        shuffle(neighbours)

        for cell in neighbours:
            if cell.visited == False:  # choose a random unvisited cell
                next_cell = cell
                cellStack.append(currentCell)
                next_cell.set_visited()
                currentCell.remove_walls(next_cell)
                currentCell = next_cell
                break
        else:
            # if there are cells no that is not visited
            currentCell = cellStack.pop()

    yield maze, False


def BFS(maze):
    """
    Return a complete maze using BFS.
    """
    n, m = maze.n, maze.m
    queue = []
    visited_path = {}
    maze.frontier = queue

    if not maze.solution_path:
        queue = [maze.start]
        visited_path[(maze.start.i, maze.start.j)] = 1
        maze.start.set_visited()
    else:
        for cell in maze.solution_path:
            cell.set_visited()
            queue.append(cell)
            visited_path[(cell.i, cell.j)] = 1

    parent = {}
    while queue:
        yield maze, True
        cur = queue.pop(0)
        visited_path[(cur.i, cur.j)] = 1
        cur.set_visited()
        if (len(visited_path) >= n * m):
            break

        neighbours = maze.get_neighbours(cur)
        shuffle(neighbours)

        for cell in neighbours:
            # Randomly choose one valid adjacent cell
            if (cell.i, cell.j) not in visited_path:
                cur.remove_walls(cell)
                queue.append(cell)
                visited_path[(cell.i, cell.j)] = 1
                cell.set_visited()
                parent[(cell.i, cell.j)] = (cur.i, cur.j)
                break

        # If there are no valid adjacent cells, we push the parent of the current cell into the queue
        else:
            if len(visited_path) < n * m:
                if (cur.i, cur.j) in parent:
                    queue.append(maze.cell_at(*parent[(cur.i, cur.j)]))

    yield maze, False


def rBFS(maze, reduced=11/16):
    """
    Return a complete maze using BFS.
    """
    n, m = maze.n, maze.m
    queue = []
    visited_path = {}
    maze.frontier = queue

    if not maze.solution_path:
        queue = [maze.start]
        visited_path[(maze.start.i, maze.start.j)] = 1
    else:
        for cell in maze.solution_path:
            queue.append(cell)
            cell.set_visited()
            visited_path[(cell.i, cell.j)] = 1

    shuffle(queue)
    saved_queue = queue[:int(reduced * len(queue))][:]
    queue[:int(reduced * len(queue))] = []

    parent = {}
    while len(visited_path) < n * m:  # Goal check

        while queue:
            yield maze, True
            cur = queue.pop(0)
            visited_path[(cur.i, cur.j)] = 1
            cur.set_visited()

            neighbours = maze.get_neighbours(cur)
            shuffle(neighbours)

            for cell in neighbours:
                # Randomly choose one valid adjacent cell
                if (cell.i, cell.j) not in visited_path:
                    cur.remove_walls(cell)
                    queue.append(cell)
                    visited_path[(cell.i, cell.j)] = 1
                    cell.set_visited()
                    parent[(cell.i, cell.j)] = (cur.i, cur.j)
                    break

            # If there are no valid adjacent cells, we push the parent of the current cell into the queue
            else:
                if len(visited_path) < n * m:
                    if (cur.i, cur.j) in parent:
                        queue.append(maze.cell_at(*parent[(cur.i, cur.j)]))

        # If the queue is empty, we add a cell in the saved queue to the queue
        queue.append(saved_queue.pop(0))

    yield maze, False
