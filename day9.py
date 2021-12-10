"""
--- Day 9: Smoke Basin ---
These caves seem to be lava tubes. Parts are even still volcanically active; small hydrothermal vents release smoke into the caves that slowly settles like rain.

If you can model how the smoke flows through the caves, you might be able to avoid it and be that much safer. The submarine generates a heightmap of the floor of the nearby caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678
Each number corresponds to the height of a particular location, where 9 is the highest and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than any of its adjacent locations. Most locations have four adjacent locations (up, down, left, and right); locations on the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal locations do not count as adjacent.)

In the above example, there are four low points, all highlighted: two are in the first row (a 1 and a 0), one is in the third row (a 5), and one is in the bottom row (also a 5). All other locations on the heightmap have some lower adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, the risk levels of the low points are 2, 1, 6, and 6. The sum of the risk levels of all low points in the heightmap is therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk levels of all low points on your heightmap?
"""
import numpy as np
from scipy.signal import argrelmin
import cv2
import matplotlib.pyplot as plt
from skimage.segmentation import watershed

def create_local_minima_mask(heightmap: np.ndarray) -> np.ndarray:
    minima_mask = np.ones_like(heightmap)
    for axis in [0, 1]:
        temp_minima_mask = np.zeros_like(heightmap)
        temp_minima_mask[argrelmin(heightmap, axis=axis)] = 1
        minima_mask = minima_mask * temp_minima_mask
    return minima_mask

def part_1(heightmap):
    minima_mask = create_local_minima_mask(heightmap)
    minimas = minima_mask * heightmap
    answer = np.sum(minimas + minima_mask)
    print(f'part 1 answer: {answer}')

def part2(heightmap):
    # visualize the height map
    plt.figure(0)
    plt.imshow(heightmap, cmap='gray')
    plt.title('heightmap')

    # find the local minima to use as markers
    minima_mask = create_local_minima_mask(heightmap)
    markers = minima_mask.ravel().cumsum().reshape(minima_mask.shape) * minima_mask
    markers = np.uint8(markers)
    plt.figure(1)
    plt.imshow(markers)
    plt.title('local minima markers')

    # apply watershed to identify basins
    basins = watershed(heightmap, markers)

    # set areas of height 9 to not belong to any basin
    basins[heightmap == 9] = 0
    print(basins)
    plt.figure(2)
    plt.imshow(basins)
    plt.title(basins)

    # determine area of each basin
    basin_sizes = np.bincount(basins.ravel())[1:]
    three_biggest_basins = np.sort(basin_sizes)[-3:]
    print(f'basin_sizes: {basin_sizes}')
    print(f'three biggest basins: {three_biggest_basins}')

    # determine the answer
    answer = 1
    for x in three_biggest_basins:
        answer = answer * x
    print(f'part 2 answer: {answer}')
    # show all figures
    plt.show()
    return answer


if __name__ == '__main__':
    with open('day9_input.txt') as f:
        lines = f.readlines()
    heightmap = np.array([[int(s) for s in line.replace('\n','')] for line in lines])
    heightmap = np.pad(heightmap, pad_width=(1,), mode='constant', constant_values=9)
    heightmap = np.uint8(heightmap)
    part_1(heightmap)
    part2(heightmap)

