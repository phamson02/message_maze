from .maze import Maze
from .combine import combine_vertically, combine_horizontally
from .random_path import random_pattern
from random import randint


class MessageSolutionPath:

    def __init__(self, message: str):
        self.lines_list = self._read_input(message)
        self.line_height = None
        self.line_width = None
        self.extension = 10
        self.maze = self._to_maze()
        self.solution_path = self.maze.solution_path

    def _to_char(self, str_line: str) -> list:
        '''Returns a list of characters of the given string'''
        chars_list = []
        for word in str_line.split():
            for char in word:
                chars_list.extend([char, 'sep'])
            chars_list.pop()
            chars_list.append('space')
        chars_list.pop()
        return chars_list

    def _read_input(self, message: str) -> list:
        '''Returns list of character list on each line of the message'''
        words_list = message.upper().split()

        words_length = [len(i) for i in words_list]
        num_words = len(words_list)
        lines_list = []
        max_line = 14
        count = 0
        current_line = []

        if num_words == 1:
            return [self._to_char(words_list[0])]
        else:
            for i in range(num_words):
                count = count + words_length[i] + 1

                if count <= max_line:
                    current_line.append(words_list[i])
                elif len(words_list[i]) >= max_line:
                    if i != 0 and len(words_list[i-1]) < max_line:
                        lines_list.append(current_line)
                    lines_list.append([words_list[i]])
                    count = 0
                else:
                    lines_list.append(current_line)
                    current_line = [words_list[i]]
                    count = words_length[i]

                if i == num_words - 1 and count == max_line:
                    lines_list.append(current_line)

                if i == num_words - 1 and count < max_line:
                    if len(words_list[i]) < max_line:
                        lines_list.append(current_line)

            lines_list = [" ".join(i) for i in lines_list]

            return [self._to_char(i) for i in lines_list]

    def _import_pattern(self, characters_list: list) -> list:
        '''Import pattern files stored and return list of Maze objects'''
        pattern_list = []
        print(characters_list)
        for char in characters_list:
            pattern_list.append(Maze.from_file(char))
        return pattern_list

    def _make_row(self, char_mazes_list: list, start: tuple, end: tuple) -> Maze:
        '''Return a row maze by combining left random-path maze, character maze and right random-path maze'''
        chars_maze = combine_horizontally(char_mazes_list)

        left_padding = (self.line_width - chars_maze.shape[1]) // 2
        right_padding = self.line_width - chars_maze.shape[1] - left_padding
        left_maze_size = (chars_maze.shape[0], left_padding)
        right_maze_size = (chars_maze.shape[0], right_padding)

        if start[1] < end[1]:
            left_maze_start = start
            left_maze_end = (chars_maze.start_cell().i, left_maze_size[1]-1)

            left_maze = random_pattern(
                left_maze_size, left_maze_start, left_maze_end)

            right_maze_start = (chars_maze.end_cell().i, 0)
            right_maze_end = (
                end[0], end[1] - left_maze_size[1] - chars_maze.shape[1])

            right_maze = random_pattern(
                right_maze_size, right_maze_start, right_maze_end)

        if start[1] > end[1]:
            left_maze_start = (chars_maze.start_cell().i, left_maze_size[1]-1)
            left_maze_end = end

            left_maze = random_pattern(
                left_maze_size, left_maze_end, left_maze_start)

            right_maze_start = (start[0], start[1] -
                                left_maze_size[1] - chars_maze.shape[1])
            right_maze_end = (chars_maze.end_cell().i, 0)

            right_maze = random_pattern(
                right_maze_size, right_maze_end, right_maze_start)

        row = combine_horizontally([left_maze, chars_maze, right_maze])

        if start[1] > end[1]:
            tmp = row.start_cell()
            row.set_start(row.end_cell().i, row.end_cell().j)
            row.set_end(tmp.i, tmp.j)

        return row

    def _to_maze(self) -> Maze:

        char_mazes_lists = []
        for line in self.lines_list:
            char_mazes_lists.append(self._import_pattern(line))

        self.line_width = max(sum(char.shape[1] for char in char_mazes_lists[i])
                              for i in range(len(char_mazes_lists)))
        self.line_width += self.extension
        self.line_height = char_mazes_lists[0][0].shape[0]

        if len(self.lines_list) == 1:
            start = (0, 0)
            end = (self.line_height-1, self.line_width-1)
            return self._make_row(char_mazes_lists[0], start, end)

        else:
            mazes_list = []
            first_start = (0, 0)
            first_end = (self.line_height-1, self.line_width -
                         randint(1, self.extension//2-1))
            first_row = self._make_row(
                char_mazes_lists[0], first_start, first_end)
            mazes_list.append(first_row)

            curr_end = first_end
            for i in range(1, len(char_mazes_lists)-1):
                if i % 2 != 0:
                    curr_start = (0, curr_end[1])
                    curr_end = (self.line_height-1,
                                randint(0, self.extension//2-2))
                    curr_row = self._make_row(
                        char_mazes_lists[i], curr_start, curr_end)
                    mazes_list.append(curr_row)

                else:
                    curr_start = (0, curr_end[1])
                    curr_end = (self.line_height-1, self.line_width -
                                randint(1, self.extension//2-1))
                    curr_row = self._make_row(
                        char_mazes_lists[i], curr_start, curr_end)
                    mazes_list.append(curr_row)

            last_start = (0, curr_end[1])
            if len(char_mazes_lists) % 2 == 1:
                last_end = (self.line_height-1, self.line_width-1)
            else:
                last_end = (self.line_height-1, 0)

            last_row = self._make_row(
                char_mazes_lists[-1], last_start, last_end)
            mazes_list.append(last_row)

            return combine_vertically(mazes_list)


def main():
    m = MessageSolutionPath('cup bob qatar')


if __name__ == '__main__':
    main()
