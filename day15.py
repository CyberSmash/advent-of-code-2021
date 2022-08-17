from typing import List, Tuple, Optional
import sys
data = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

ROW_IDX = 0
COL_IDX = 1
WEIGHT_IDX = 2


class Node(object):
    def __init__(self, row, col, cost):
        self.row = row
        self.col = col
        self.cost = cost
        self.neighbors = list()
        self.distance = 999999
        self.prev = None

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

    def get_neighbors(self):
        return self.neighbors

    def get_sorted_neighbors(self):
        return sorted(self.neighbors, key=lambda node: node.cost)

    def __str__(self):
        out = f"({self.row}, {self.col}) - {self.cost}"
        return out

    def __repr__(self):
        return self.__str__()


class Grid(object):
    def __init__(self, data):

        data_lines = data.split("\n")
        self.grid = list()
        for r, line in enumerate(data_lines):
            self.grid.append(list())
            for c, cost in enumerate(line):
                n = Node(r, c, int(cost))
                self.grid[-1].append(n)

        # TODO: This assumes a rectangular grid.
        self.max_rows = len(self.grid) - 1
        self.max_cols = len(self.grid[0]) - 1

        self.max_virtual_rows = 0
        self.max_virtual_cols = 0

        for row in self.grid:
            for node in row:
                neighbors = self.get_neighbors(node)
                node.set_neighbors(neighbors)

        self.repeat_size = 1

    def get_location_cost(self, row: int, col: int) -> Optional[int]:
        """
        Get the cost of a location from the grid.

        N.B. This is the proper way to access the grid.

        :param row: The row value
        :param col: The column value
        :return: None if row/col is out of bounds. The value if it's in bounds.
        """
        if row < 0 or col < 0:
            return None

        # We are outside of the virtual grid.
        if row > self.max_virtual_rows or col > self.max_virtual_cols:
            return None

        # We are inside the physical grid. Just return the cost directly.
        if self.max_rows >= row >= 0 and self.max_cols >= col >= 0:
            return self.grid[row][col].cost

        # In this case we are somewherein the virtual grid. Calculate the value.

        # Get the original grid location value.
        phys_grid_row = row % (self.max_rows + 1)
        phys_grid_col = col % (self.max_cols + 1)
        initial_cost = self.grid[phys_grid_row][phys_grid_col].cost

        # determine what grid we're in:
        grid_row_num = row // (self.max_rows + 1)
        grid_col_num = col // (self.max_cols + 1)

        addition = 0
        prev_val = 0
        if grid_col_num > 0 and grid_row_num > 0:
            prev_val = self.get_location_cost(row - 10, col - 10)
            addition = 2
        elif grid_col_num > 0 and grid_row_num == 0:
            prev_val = self.get_location_cost(row, col - 10)
            addition = 1
        elif grid_col_num == 0 and grid_row_num > 0:
            prev_val = self.get_location_cost(row - 10, col)
            addition = 1

        if addition == 1 and prev_val == 9:
            return 1
        elif addition == 2 and prev_val == 9:
            return 2
        elif addition == 2 and prev_val == 8:
            return 1
        else:
            return prev_val + addition

    def set_repeat_size(self, size):
        self.repeat_size = size
        self.max_virtual_rows = self.repeat_size * (self.max_rows + 1)
        self.max_virtual_cols = self.repeat_size * (self.max_cols + 1)

    def get_neighbors(self, current_node) -> List:
        neighbors = list()
        current_row = current_node.row
        current_col = current_node.col

        if current_row > 0:
            neighbors.append(self.grid[current_row - 1][current_col])
        if current_col > 0:
            neighbors.append(self.grid[current_row][current_col - 1])
        if current_col < self.max_cols:
            neighbors.append(self.grid[current_row][current_col + 1])
        if current_row < self.max_rows:
            neighbors.append(self.grid[current_row + 1][current_col])

        return neighbors

    def get_neighbors_by_coords(self, row, col):
        neighbors = list()
        if row > 0:
            neighbors.append((row - 1, col))
        if col > 0:
            neighbors.append((row, col - 1))
        if col < self.max_cols:
            neighbors.append((row, col + 1))
        if row < self.max_rows:
            neighbors.append((row + 1, col))
        return neighbors


    def setup_unexplored(self) -> List:
        """
        Returns a node list of lists with the indexes being:
        0: row
        1: column
        2: Distance
        :param grid: The grid.
        :return:
        """
        unexplored = list()
        # Plus 1 here because range is non-inclusive.
        for row in self.grid:
            for node in row:
                unexplored.append(node)

        return unexplored

    def path_find(self, start_node, end_node):
        unexplored = self.setup_unexplored()
        neighbors = start_node.get_sorted_neighbors()
        visited_list: List = list()
        start_node.distance = 0

        while len(unexplored) > 0:
            next_node: Node = min(unexplored, key=lambda n: n.distance)
            visited_list.append(next_node)
            unexplored.remove(next_node)
            neighbors = next_node.get_sorted_neighbors()
            for neighbor in neighbors:
                if neighbor in visited_list:
                    continue

                current_distance = neighbor.cost + next_node.distance
                if current_distance < neighbor.distance:
                    neighbor.distance = current_distance
                    neighbor.prev = next_node

        print(f"End node distance: {end_node.distance}")
        print("Shortest Path: ")
        current_node = end_node
        while current_node != start_node:
            print(current_node)
            current_node = current_node.prev

    def __str__(self):
        out = ""
        for r in self.grid:
            for node in r:
                print(f"{node.cost} ", end="")
            print("")
        return out

    def __repr__(self):
        return self.__str__()



def main():

    #with open("./chiton.txt", "r") as fp:
    #    data = fp.read()

    grid = Grid(data)
    grid.set_repeat_size(5)
    print(grid.get_location_cost(0, 0))
    print(grid.get_location_cost(9, 9))
    print(grid.get_location_cost(10, 10))
    print(grid.get_location_cost(11, 11))
    for r in range(50):
        for c in range(50):
            print(grid.get_location_cost(r, c), end=" ")
        print("")

    #print(grid)
    #print(grid.grid[1][1].get_sorted_neighbors())
    #grid.path_find(grid.grid[0][0], grid.grid[99][99])



if __name__ == "__main__":
    main()