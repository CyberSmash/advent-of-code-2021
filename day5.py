import re
import numpy
import math
class Vector2(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"({self.x}, {self.y})"


class Segment(object):
    def __init__(self, start: Vector2, end: Vector2):
        self.start = start
        self.end = end

    def direction(self) -> Vector2:
        """
        TODO: This could be done with magnitude and normalization.
        :return:
        """
        ret = Vector2(0, 0)
        x = self.end.x - self.start.x
        if x < 0:
            ret.x = -1
        elif x == 0:
            ret.x = 0
        elif x > 0:
            ret.x = 1

        y = self.end.y - self.start.y
        if y < 0:
            ret.y = -1
        elif y == 0:
            ret.y = 0
        elif y > 0:
            ret.y = 1

        return ret

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.start} -> {self.end}"

class Grid(object):
    def __init__(self, x_size, y_size):
        self.grid = numpy.zeros((x_size, y_size))

    def inc_loc(self, x, y):
        # Gotta flip y major axis to work how we expect.
        self.grid[y][x] += 1

    def plot_segment(self, segment: Segment):
        direction = segment.direction()

        current_point = segment.start
        while 1:
            if current_point.x == segment.end.x and current_point.y == segment.end.y:
                self.inc_loc(current_point.x, current_point.y)
                break
            self.inc_loc(current_point.x, current_point.y)
            current_point.x += direction.x
            current_point.y += direction.y

    def count_overlaps(self):
        overlaps = 0
        for x in self.grid:
            for y in x:
                if y > 1:
                    overlaps += 1

        return overlaps

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.grid)


def main():
    r = re.compile("([0-9].*?),([0-9].*?) -> ([0-9].*?),([0-9].*)")
    segments = list()
    g = Grid(1000, 1000)
    with open("./points.txt", "r") as fp:

        for line in fp:
            line = line.strip()
            m = r.search(line)

            start = Vector2(int(m.group(1)), int(m.group(2)))
            end = Vector2(int(m.group(3)), int(m.group(4)))
            segment = Segment(start, end)
            #direction = segment.direction()
            #if direction.x != 0 and direction.y != 0:
                # Ensure this is only horizontal or vertical, ignore
                # diagonal lines
            #    continue
            segments.append(segment)

    for segment in segments:
        g.plot_segment(segment)

    overlaps = g.count_overlaps()
    print(f"Number of overlaps: {overlaps}")
    #print(g)


if __name__ == "__main__":
    main()