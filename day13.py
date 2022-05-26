import os
import re
from typing import Optional, List
data = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()


def print_grid(grid: List[List[str]]):
    for r in grid:
        for c in r:
            print(c, end="")
        print("")
    print("")


def fill_grid(grid: List[List[str]], points) -> List[List[str]]:
    for point in points:
        grid[point.y][point.x] = '#'
    return grid


def fold_on_y(grid, fold_line):
    line_len = len(grid[fold_line])
    grid[fold_line] = '-' * line_len
    num_lines = len(grid)

    above_line = fold_line - 1
    below_line = fold_line + 1
    print(f"Folding from {below_line} to {num_lines}")
    for r in range(below_line, num_lines):
        for c in range(0, line_len):
            if grid[r][c] == '#':
                grid[above_line][c] = grid[r][c]
        above_line -= 1

    grid = grid[:fold_line]

    return grid

def count_dots(grid) -> int:
    num_dots = 0
    for r in grid:
        for c in r:
            if c == '#':
                num_dots += 1
    return num_dots

def fold_on_x(grid, fold_line):
    line_len = len(grid)
    row_len = len(grid[0])
    for x in range(line_len):
        grid[x][fold_line] = "|"

    num_lines = len(grid)

    left_line = fold_line - 1
    right_line = fold_line + 1
    for r in range(0, num_lines):
        current_left_line = left_line
        for c in range(right_line, row_len):
            if grid[r][c] == '#':
                grid[r][current_left_line] = '#'
            current_left_line -= 1
    for idx in range(num_lines):
        grid[idx] = grid[idx][:fold_line]
    return grid


def main():
    fold_re = re.compile("fold along (x|y)=([0-9]*)")

    with open("transparency.txt", "r") as fp:
        data = fp.read()
    data_lines = data.split(os.linesep)

    points: List[Point] = list()
    folds = list()
    for line in data_lines:
        if "," in line:
            x, y = line.split(",")
            points.append(Point(int(x), int(y)))
        elif "=" in line:
            m = fold_re.match(line)
            direction = m.group(1)
            line = int(m.group(2))
            folds.append((direction, line))

    max_x = max(points, key=lambda p: p.x)
    max_y = max(points, key=lambda p: p.y)

    grid = [[' ' for _ in range(max_x.x + 1)] for _ in range(max_y.y + 1)]
    fill_grid(grid, points)
    print(f"Max X {max_x.x} Max Y {max_y.y}")
    for fold in folds:
        if fold[0] == 'y':
        #print_grid(grid)
            print(f"Folding on y : {fold[1]}")
            grid = fold_on_y(grid, fold[1])
        else:
            print(f"Folding on x : {fold[1]}")
            grid = fold_on_x(grid, fold[1])

    print_grid(grid)
    #grid = fold_on_x(grid, folds[1][1])
    #print_grid(grid)

    print(f"Number of dots: {count_dots(grid)}")


if __name__ == '__main__':
    main()

