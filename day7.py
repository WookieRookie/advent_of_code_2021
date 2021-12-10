"""
--- Day 7: The Treachery of Whales ---
A giant whale has decided your submarine is its next meal, and it's much faster than you are. There's nowhere to run!

Suddenly, a swarm of crabs (each in its own tiny submarine - it's too deep for them otherwise) zooms in to rescue you! They seem to be preparing to blast a hole in the ocean floor; sensors indicate a massive underground cave system just beyond where they're aiming!

The crab submarines all need to be aligned before they'll have enough power to blast a large enough hole for your submarine to get through. However, it doesn't look like they'll be aligned before the whale catches you! Maybe you can help?

There's one major catch - crab submarines can only move horizontally.

You quickly make a list of the horizontal position of each crab (your puzzle input). Crab submarines have limited fuel, so you need to find a way to make all of their horizontal positions match while requiring them to spend as little fuel as possible.

For example, consider the following horizontal positions:

16,1,2,0,4,2,7,1,2,14
This means there's a crab with horizontal position 16, a crab with horizontal position 1, and so on.

Each change of 1 step in horizontal position of a single crab costs 1 fuel. You could choose any horizontal position to align them all on, but the one that costs the least fuel is horizontal position 2:

Move from 16 to 2: 14 fuel
Move from 1 to 2: 1 fuel
Move from 2 to 2: 0 fuel
Move from 0 to 2: 2 fuel
Move from 4 to 2: 2 fuel
Move from 2 to 2: 0 fuel
Move from 7 to 2: 5 fuel
Move from 1 to 2: 1 fuel
Move from 2 to 2: 0 fuel
Move from 14 to 2: 12 fuel
This costs a total of 37 fuel. This is the cheapest possible outcome; more expensive outcomes include aligning at position 1 (41 fuel), position 3 (39 fuel), or position 10 (71 fuel).

Determine the horizontal position that the crabs can align to using the least fuel possible. How much fuel must they spend to align to that position?
"""
import numpy as np
from typing import Callable


def solve_problem(positions: np.ndarray, cost_function: Callable[[int], int]):
    target_position = np.median(positions)
    distance_to_target = np.abs(positions - target_position)
    cost = np.vectorize(cost_function)(distance_to_target).sum()
    print(f'target location: {target_position}')
    print(f'total cost: {cost}')
    return cost


def for_loop_method(positions, cost_function):
    costs = []
    for target in range(0, int(positions.max())):
        distance = np.abs(positions - target)
        cost = np.vectorize(cost_function)(distance).sum()
        costs.append(cost)
    costs = np.array(costs)
    answer = costs.min()
    print(f'lowest cost location: {costs.argmin()}')
    print(f'fuel cost to get to target: {answer}')
    return answer


if __name__ == '__main__':
    with open('day7_input.txt') as f:
        line = f.readline()
    print(line)
    positions = np.fromstring(line, sep=',')
    # answer1_fl = for_loop_method(positions, lambda x: x)
    # answer2_fl = for_loop_method(positions, lambda x: x*(x+1)/2)
    answer1 = solve_problem(positions, lambda x: x)
    print(f'answer to part 1: {answer1}')
    answer2 = for_loop_method(positions, lambda x: x*(x+1)/2)
    print(f'answer to part 2: {answer2}')

