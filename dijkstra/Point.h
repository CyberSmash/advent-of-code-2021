//
// Created by jordan on 7/6/22.
//

#ifndef DIJKSTRA_POINT_H
#define DIJKSTRA_POINT_H

#define INF 0x3f3f3f3f

class Point {
public:
    Point(int row, int col, int cost);
    Point(int row, int col, int cost, int dist, Point* prev);
    int get_cost() const;
    int get_row() const;
    int get_col() const;

    void set_dist(int distance);
    void set_prev(Point* p);
    Point* get_prev() const;
    virtual ~Point() = default;

private:
    int row;
    int col;
    int cost;
public:
    void set_cost(int cost);

private:
    int dist;
public:
    int get_dist() const;

private:
    Point* prev; // TODO: Should this be a raw pointer;
};


#endif //DIJKSTRA_POINT_H
