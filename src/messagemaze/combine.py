from .maze import Maze

def combine_horizontally(mazes_list: list):
    '''Combine Maze objects horizontally'''
    maze_height = mazes_list[0].shape[0]
    maze_width = 0

    for a in mazes_list:
        maze_width += a.shape[1]
        assert maze_height == a.shape[0], "Maze heights are not the same"

    c = Maze(maze_height, maze_width)
    maze_cells_a = mazes_list[0].get_cells()
    j = 1
    width_temp = 0

    while j < len(mazes_list):
        temp_cell = mazes_list[j].get_cells()
        width_temp += mazes_list[j-1].shape[1]

        # Update the position of the cells
        for elem in temp_cell:
            for cell_obj in elem:
                cell_obj.j += width_temp

        # Connect mazes by breaking walls between start and end cells
        mazes_list[j-1].end_cell().remove_walls(mazes_list[j].start_cell())

        for i in range(maze_height):
            maze_cells_a[i].extend(temp_cell[i])

        j = j + 1

    # Set start and end cells of the combined maze
    c.set_cells(maze_cells_a)
    c.set_start(mazes_list[0].start_cell().i, mazes_list[0].start_cell().j)
    c.set_end(mazes_list[-1].end_cell().i, mazes_list[-1].end_cell().j)
    for maze in mazes_list:
        c.solution_path.extend(maze.solution_path)

    return c


def combine_vertically(mazes_list: list):
    '''Combine Maze objects vertically'''
    maze_width = mazes_list[0].shape[1]
    maze_height = 0

    for a in mazes_list:
        maze_height += a.shape[0]
        assert maze_width == a.shape[1], "Maze widths are not the same"

    c = Maze(maze_height, maze_width)
    maze_cells_a = mazes_list[0].get_cells()
    j = 1
    height_temp = 0

    while j < len(mazes_list):
        temp_cell = mazes_list[j].get_cells()
        height_temp += mazes_list[j-1].shape[0]

        # Update the position of the cells
        for elem in temp_cell:
            for cell_obj in elem:
                cell_obj.i += height_temp

        # Connect mazes by breaking walls between start and end cells
        mazes_list[j-1].end_cell().remove_walls(mazes_list[j].start_cell())

        maze_cells_a.extend(temp_cell)

        j = j + 1

    # Set start and end cells of the combined maze
    c.set_cells(maze_cells_a)
    c.set_start(mazes_list[0].start_cell().i, mazes_list[0].start_cell().j)
    c.set_end(mazes_list[-1].end_cell().i, mazes_list[-1].end_cell().j)

    for maze in mazes_list:
        c.solution_path.extend(maze.solution_path)

    return c
