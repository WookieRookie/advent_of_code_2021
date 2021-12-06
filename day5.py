"""
--- Day 5: Hydrothermal Venture ---
You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce large, opaque clouds, so it would be best to avoid them if possible.

They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end the line segment and x2,y2 are the coordinates of the other end. These line segments include the points at both ends. In other words:

An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....
In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is shown as the number of lines which cover that point or . if no line covers that point. The top-left pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap. In the above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two lines overlap?

--- Part Two ---
Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture; you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your list will only ever be horizontal, vertical, or a diagonal line at exactly 45 degrees. In other words:

An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
Considering all lines from the above example would now produce the following diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....
You still need to determine the number of points where at least two lines overlap. In the above example, this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?

"""
from collections import namedtuple
import numpy as np
from operator import xor

LineSegmentTuple = namedtuple('LineSegment', ['x1', 'y1', 'x2', 'y2'])

class LineSegment:
    def __init__(self, line, mask_shape = (1000, 1000)):
        self.line = line
        self.x1, self.y1, self.x2, self.y2 = np.fromstring(line.replace(' -> ', ','), sep=',', dtype=int)
        self.delta_x = self.x2 - self.x1
        self.delta_y = self.y2 - self.y1
        self.slope = (self.delta_y / self.delta_x) if self.delta_x != 0 else 0
        if abs(self.delta_y)<abs(self.delta_x):
            rng = np.arange(min(0, self.delta_x), max(1, self.delta_x+1))
            x_coords = rng + self.x1
            y_coords = self.slope * rng + self.y1
        else:
            rng = np.arange(min(0, self.delta_y), max(1, self.delta_y+1))
            x_coords = self.slope * rng + self.x1
            y_coords = rng + self.y1
        self.x_coords = x_coords.astype(int)
        self.y_coords = y_coords.astype(int)
        mask = np.zeros(mask_shape)
        mask[self.x_coords, self.y_coords] = 1
        # if(mask.sum()==0):
        # print(line)
        # print(mask)
        # print('------------')
        self.mask = mask

    def __repr__(self):
        return f'{self.line} | ({self.x1}, {self.y1}), ({self.x2}, {self.y2})'

# def parse_line(line:str):
#     coords = np.fromstring(line.replace(' -> ', ','), sep=',', dtype=int)
#     return LineSegmentTuple(*coords)


def part_1(lines):
    line_segments = [LineSegment(line) for line in lines]
    valid_line_segments = []
    [valid_line_segments.append(ls) for ls in line_segments if ((ls.delta_x)==0 or (ls.delta_y==0))]
    field = np.zeros((1000, 1000))
    for ls in valid_line_segments:
        field[ls.x_coords, ls.y_coords] += 1
    print(field)
    print(np.sum(field>=2))

    # line_segments = [parse_line(line) for line in lines]
    # field = np.zeros((10, 10))
    # for ls in line_segments:
    #     print(ls)
    #     if xor((ls.x1==ls.x2),(ls.y1==ls.y2)):
    #         line_segment_mask = np.zeros_like(field)
    #         line_segment_mask[ls.x1:ls.x2+1, ls.y1:ls.y2+1] += 1
    #         print(line_segment_mask)
    #         field = field + line_segment_mask
    #         print(field)
    #         print('----------')
    # print(line_segments[0])
    # print(field)
    # print(np.sum(field>=2))

def part_2(lines):
    line_segments = [LineSegment(line) for line in lines]
    field = np.zeros((1000, 1000))
    for ls in line_segments:
        field[ls.x_coords, ls.y_coords] += 1
    print(field)
    print(np.sum(field >= 2))

if __name__ == '__main__':
    with open('day5_input.txt') as f:
    # with open('day5_testinput.txt') as f:
        lines = f.readlines()
    # part_1(lines)
    part_2(lines)