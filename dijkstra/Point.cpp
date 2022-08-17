//
// Created by jordan on 7/6/22.
//

#include "Point.h"

Point::Point(int row, int col, int cost) : row(row), col(col), cost(cost), dist(INF), prev(nullptr)
{

}

Point::Point(int row, int col, int cost, int dist, Point* prev) : row(row), col(col), cost(cost), dist(dist), prev(prev) {

}


int Point::get_cost() const
{
    return cost;
}

int Point::get_row() const
{
    return row;
}

int Point::get_col() const
{
    return col;
}

void Point::set_prev(Point *p)
{
    prev = p;
}

void Point::set_dist(int distance)
{
    dist = distance;
}

int Point::get_dist() const {
    return dist;
}

void Point::set_cost(int cost) {
    Point::cost = cost;
}



