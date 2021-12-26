import pygame
from .maze import Maze


def _show_pattern(pattern: Maze, screen, thick=2):
    w = min(screen.get_height()//pattern.n, screen.get_width()//pattern.m)
    for row in pattern.cells:
        for cell in row:
            y = cell.i * w
            x = cell.j * w
            if cell in pattern.solution_path:
                pygame.draw.rect(screen, 'Red', (x, y, w, w))
            if cell.walls['N']:
                pygame.draw.line(screen, 'Black', (x, y), (x+w, y), thick)
            if cell.walls['E']:
                pygame.draw.line(screen, 'Black', (x+w, y), (x+w, y+w), thick)
            if cell.walls['S']:
                pygame.draw.line(screen, 'Black', (x+w, y+w), (x, y+w), thick)
            if cell.walls['W']:
                pygame.draw.line(screen, 'Black', (x, y+w), (x, y), thick)


def DrawPattern(name: str, size: tuple = (13, 13), save_file=False, screen_size: tuple = (400, 400)):
    '''
    Draw the pattern. Press Ctrl+Z to undo a step. Press Space to either return pattern or save pattern to file.

    Parameters
    ----------
    name : str
        Name of the pattern
    size : tuple, optional
        Size of the pattern. The default is (13, 13).
    save_file : bool, optional
        Save the pattern to subfolder "patterns". The default is False.
    screen_size : tuple, optional
        Size of the screen. The default is (400, 400).
    '''
    m, n = size
    pattern = Maze.Blank(m, n)
    running = True

    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    w = min(screen.get_height()//pattern.n, screen.get_width()//pattern.m)

    while running:
        for event in pygame.event.get():
            # Close to quit the program
            if event.type == pygame.QUIT:
                running = False

            # Click to add a cell to the path
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    try:
                        # Get cell indexes
                        j = pos[0] // w
                        i = pos[1] // w

                        curr = pattern.cells[i][j]
                        is_added = True
                    except IndexError:
                        print('Pick a cell')
                        continue

                    if curr not in pattern.solution_path:
                        pattern.solution_path.append(curr)

                        if len(pattern.solution_path) > 1:
                            # Check if the current cell is adjacent to the previous cell
                            if prev.remove_walls(curr) == -1:
                                pattern.solution_path.remove(curr)
                                is_added = False

                        if is_added:
                            prev = curr

            if event.type == pygame.KEYDOWN:

                # Press Ctrl + Z to undo the last cell
                if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:

                    if len(pattern.solution_path) == 0:
                        print('No more steps to undo')

                    # If there is only one cell in the path,
                    # just remove it and set univisited
                    elif len(pattern.solution_path) == 1:
                        first = pattern.solution_path.pop()
                        print('Undo the last step')

                    # If there are more than one cells in the path,
                    # remove the last cell, add walls and set univisited
                    else:
                        out = pattern.solution_path.pop()
                        prev = pattern.solution_path[-1]

                        prev.add_walls(out)
                        print('Undo the last step')

                # Press Space to save the pattern
                if event.key == pygame.K_SPACE:

                    if save_file == True:
                        pattern.start = pattern.solution_path[0]
                        pattern.end = pattern.solution_path[-1]
                        pattern.to_file(name)
                        print('Pattern saved to file')
                        return None
                    else:
                        pattern.start = pattern.solution_path[0]
                        pattern.end = pattern.solution_path[-1]
                        print('Pattern returned')
                        return pattern

        screen.fill('white')
        _show_pattern(pattern, screen)
        pygame.display.update()
