//
// Created by jordan on 7/6/22.
//

#include "Grid.h"
#include <list>
#include <queue>
Grid::Grid(const std::vector<std::string>& data_lines)
{
    // Reserve the rows
    grid.resize(data_lines.size());
    for(int i = 0; i < data_lines.size(); i++)
    {
        // Reserve the columns.
        grid[i].reserve(data_lines[i].length());

        for (int j = 0; j < data_lines[i].length(); j++)
        {
            int cost = data_lines[i][j] - 0x30;
            grid[i].emplace_back(i, j, cost);
        }

    }

    std::cout << "Grid size: " << grid.size() << std::endl;
}

std::ostream& operator<<(std::ostream& os, const Grid& g)
{

    for (const std::vector<Point>& line : g.grid)
    {
        for (const Point& p : line)
        {
            os << p.get_cost() << " ";
        }
        os << std::endl;
    }
    return os;
}

/**
 * ew...
 *
 * @param row
 * @param col
 * @return
 */
int Grid::get_cost(int row, int col)
{
    int cost = 0;
    bool row_too_big = row / grid.size() > 0;
    bool col_too_big = col / grid[0].size() > 0;
    int adder = 1;
    if (row_too_big && col_too_big)
    {
        cost = get_cost(row - grid.size(), col - grid[0].size());
        adder = 2;
    }
    else if (!row_too_big && col_too_big)
    {
        cost = get_cost(row, col - grid[0].size());
    }
    else if (row_too_big && !col_too_big)
    {
        cost = get_cost(row - grid.size(), col);
    }
    else
    {
        return grid[row][col].get_cost();
    }

    if (cost == 9)
    {
        if (adder == 1)
            return 1;
        if (adder == 2)
            return 2;
    }
    if (cost == 8)
    {
        if (adder == 1)
            return 9;
        if (adder == 2)
            return 1;
    }

    return cost + adder;
}

void Grid::reset_grid()
{
    for (auto& line : grid)
    {
        for (auto& p : line)
        {
            p.set_prev(nullptr);
            p.set_dist(INF);
        }
    }
}

std::vector<Point*> Grid::get_neighbors(int row, int col)
{
    std::vector<Point*> neighbors(4, nullptr);

    if (row > 0)
    {
        neighbors[0] = &grid[row - 1][col];
    }
    if (col > 0)
    {
        neighbors[1] = &grid[row][col - 1];
    }
    if (row < rows())
    {
        neighbors[2] = &grid[row+1][col];
    }
    if (col < cols())
    {
        neighbors[3] = &grid[row][col+1];
    }

    return neighbors;
}

int Grid::dijkstra(int start_row, int start_col, int end_row, int end_col)
{
    reset_grid();
    //std::list<Point*> visited;
    auto comp = [](const Point *a, const Point* b){
        return a->get_dist() > b->get_dist();
    };

    std::priority_queue<Point*, std::vector<Point*>, decltype(comp)> unvisited(comp);

    grid[start_row][start_col].set_dist(0);
    grid[start_row][start_col].set_cost(0);
    unvisited.push(&grid[start_row][start_col]);

    while (!unvisited.empty())
    {

        Point* current_node = unvisited.top();
        unvisited.pop();
        if (current_node->get_row() == end_row && current_node->get_col() == end_col)
            break;

        auto neighbors = get_neighbors(current_node->get_row(), current_node->get_col());
        for (auto neighbor : neighbors)
        {
            if (neighbor == nullptr) continue;

            int total_dist = current_node->get_dist() + neighbor->get_cost();

            if (neighbor->get_dist() > total_dist)
            {
                neighbor->set_dist(total_dist);
                neighbor->set_prev(current_node);
                unvisited.push(neighbor);
            }
        }
    }

    std::cout << "Total cost: " << grid[end_row][end_col].get_dist() << std::endl;
    return grid[end_row][end_col].get_dist();
}

void Grid::extend_grid(int multiplier)
{
    std::vector<std::vector<Point>> new_grid;
    unsigned long num_rows = grid.size() * multiplier;
    unsigned long num_cols = grid[0].size() * multiplier;
    new_grid.resize(num_rows);

    for (int r = 0; r < num_rows; r++)
    {
        new_grid[r].reserve(num_cols);
        for (int c = 0; c < num_cols; c++)
        {
            new_grid[r].emplace_back(r, c, get_cost(r, c));
        }
    }

    grid = new_grid;
}

int Grid::rows() {
    return grid.size() - 1;
}

int Grid::cols() {
    return grid[0].size() - 1;
}
