//
// Created by jordan on 7/6/22.
//

#ifndef DIJKSTRA_GRID_H
#define DIJKSTRA_GRID_H
#include <vector>
#include <string>
#include <iostream>
#include "Point.h"

#define UP 1
#define DOWN 2
#define LEFT 4
#define RIGHT 8

class Grid {
public:
    explicit Grid(const std::vector<std::string>& data_lines);
    void extend_grid(int multiplier);
    friend std::ostream& operator<<(std::ostream& os, const Grid& g);
    int dijkstra(int start_row, int start_col, int end_row, int end_col);
    int rows();
    int cols();
    virtual ~Grid() = default;
private:
    std::vector<std::vector<Point>> grid;

    int get_cost(int row, int col);



    void reset_grid();

    std::vector<Point *> get_neighbors(int row, int col);
};


#endif //DIJKSTRA_GRID_H
