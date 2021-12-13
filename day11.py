"""
You enter a large cavern full of rare bioluminescent dumbo octopuses! They seem to not like the Christmas lights on your submarine, so you turn them off for now.

There are 100 octopuses arranged neatly in a 10 by 10 grid. Each octopus slowly gains energy over time and flashes brightly for a moment when its energy is full. Although your lights are off, maybe you could navigate through the cave without disturbing the octopuses if you could predict when the flashes of light will happen.

Each octopus has an energy level - your submarine can remotely measure the energy level of each octopus (your puzzle input). For example:

The energy level of each octopus is a value between 0 and 9. Here, the top-left octopus has an energy level of 5, the bottom-right one has an energy level of 6, and so on.

You can model the energy levels and flashes of light in steps. During a single step, the following occurs:


First, the energy level of each octopus increases by 1.
Then, any octopus with an energy level greater than 9 flashes. This increases the energy level of all adjacent octopuses by 1, including octopuses that are diagonally adjacent. If this causes an octopus to have an energy level greater than 9, it also flashes. This process continues as long as new octopuses keep having their energy level increased beyond 9. (An octopus can only flash at most once per step.)
Finally, any octopus that flashed during this step has its energy level set to 0, as it used all of its energy to flash.
Adjacent flashes can cause an octopus to flash on a step even if it begins that step with very little energy. Consider the middle octopus with 1 energy in this situation:

After 100 steps, there have been a total of 1656 flashes.

Given the starting energy levels of the dumbo octopuses in your cavern, simulate 100 steps. How many total flashes are there after 100 steps?
"""
import numpy as np
from scipy.signal import convolve2d

BLAST_RADIUS = np.ones((3, 3), dtype=np.uint8)

def step(cave: np.ndarray, flashed_this_step: np.ndarray, num_flashed: int, step_count, substep_count=0):
    ready_to_flash = cave > 9
    flashes = np.zeros_like(cave)
    flashes[ready_to_flash] = 1
    additional_energy_gained = convolve2d(flashes, BLAST_RADIUS, mode='same')
    cave = cave + additional_energy_gained
    flashed_this_step = np.logical_or(flashed_this_step, ready_to_flash) # octupi can only flash once per step
    cave[flashed_this_step] = 0
    num_flashed += np.sum(ready_to_flash.ravel())
    # print(f'-------- Step {step_count}.{substep_count} ------------ \n {cave}')
    if np.max(cave) > 9:
        cave, num_flashed = step(cave=cave,
                                 flashed_this_step=flashed_this_step,
                                 num_flashed=num_flashed,
                                 step_count=step_count,
                                 substep_count=substep_count+1)
    return cave, num_flashed

def part_1(cave: np.ndarray, n_steps: int):
    num_flashed = 0
    for i in range(1, n_steps+1):
        cave += np.ones_like(cave)
        flashed_this_step = np.zeros_like(cave)
        cave, num_flashed = step(cave=cave,
                                 flashed_this_step=flashed_this_step,
                                 num_flashed=num_flashed,
                                 step_count=i,
                                 substep_count=0)
        print(f'step {i}: {num_flashed} flashed')

def part_2(cave: np.ndarray):
    step_count = 0
    num_flashed = 0
    while np.max(cave)!=0:
        cave += np.ones_like(cave)
        flashed_this_step = np.zeros_like(cave)
        cave, num_flashed = step(cave=cave,
                                 flashed_this_step=flashed_this_step,
                                 num_flashed=num_flashed,
                                 step_count=step_count,
                                 substep_count=0)
        step_count += 1
        print(f'--------- step: {step_count} ----------- \n {cave}')
    print(f'part 2: {step_count}')

if __name__ == '__main__':
    with open('day11_input.txt') as f:
        lines = f.readlines()
    cave = np.array([[int(s) for s in line.replace('\n','')] for line in lines])
    cave = np.uint8(cave)
    print(cave)
    part_1(cave, n_steps=100)
    part_2(cave)
