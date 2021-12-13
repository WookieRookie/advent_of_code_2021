"""
--- Day 10: Syntax Scoring ---
You ask the submarine to determine the best route out of the deep-sea cave, but it only replies:

Syntax error in navigation subsystem on line: all of them
All of them?! The damage is worse than you thought. You bring up a copy of the navigation subsystem (your puzzle input).

The navigation subsystem syntax is made of several lines containing chunks. There are one or more chunks on each line, and chunks contain zero or more other chunks. Adjacent chunks are not separated by any delimiter; if one chunk stops, the next chunk (if any) can immediately start. Every chunk must open and close with one of four legal pairs of matching characters:

If a chunk opens with (, it must close with ).
If a chunk opens with [, it must close with ].
If a chunk opens with {, it must close with }.
If a chunk opens with <, it must close with >.
So, () is a legal chunk that contains no other chunks, as is []. More complex but valid chunks include ([]), {()()()}, <([{}])>, [<>({}){}[([])<>]], and even (((((((((()))))))))).

Some lines are incomplete, but others are corrupted. Find and discard the corrupted lines first.

A corrupted line is one where a chunk closes with the wrong character - that is, where the characters it opens and closes with do not form one of the four legal pairs listed above.

Examples of corrupted chunks include (], {()()()>, (((()))}, and <([]){()}[{}]). Such a chunk can appear anywhere within a line, and its presence causes the whole line to be considered corrupted.

For example, consider the following navigation subsystem:

[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
Some of the lines aren't corrupted, just incomplete; you can ignore these lines for now. The remaining five lines are corrupted:

{([(<{}[<>[]}>{[]{[(<()> - Expected ], but found } instead.
[[<[([]))<([[{}[[()]]] - Expected ], but found ) instead.
[{[{({}]{}}([{[{{{}}([] - Expected ), but found ] instead.
[<(<(<(<{}))><([]([]() - Expected >, but found ) instead.
<{([([[(<>()){}]>(<<{{ - Expected ], but found > instead.
Stop at the first incorrect closing character on each corrupted line.

Did you know that syntax checkers actually have contests to see who can get the high score for syntax errors in a file? It's true! To calculate the syntax error score for a line, take the first illegal character on the line and look it up in the following table:

): 3 points.
]: 57 points.
}: 1197 points.
>: 25137 points.
In the above example, an illegal ) was found twice (2*3 = 6 points), an illegal ] was found once (57 points), an illegal } was found once (1197 points), and an illegal > was found once (25137 points). So, the total syntax error score for this file is 6+57+1197+25137 = 26397 points!

Find the first illegal character in each corrupted line of the navigation subsystem. What is the total syntax error score for those errors?
"""
from collections import deque
import numpy as np

OPENERS = ['(', '[', '<', '{']
CLOSERS = [')', ']', '>', '}']
MATCHING_OPENING_CHARACTERS = {closer: opener for (closer, opener) in zip(CLOSERS, OPENERS)}
MATCHING_CLOSING_CHARACTERS = {opener: closer for (closer, opener) in zip(CLOSERS, OPENERS)}
OPENERS = set(OPENERS)
CLOSERS = set(CLOSERS)
PART1_POINT_VALUES = {')': 3,
                      ']': 57,
                      '}': 1197,
                      '>': 25137}
PART2_POINT_VALUES = {')': 1,
                      ']': 2,
                      '}': 3,
                      '>': 4}

def score_line(line: str) -> int:
    open_stack = deque()
    close_stack = deque()
    for i, c in enumerate(line):
        if c in OPENERS:
            open_stack.append(c)
        elif c in CLOSERS:
            last_opener = open_stack.pop()
            if last_opener != MATCHING_OPENING_CHARACTERS[c]:
                print(f'{c} does not match. Line {line[:i]}   {line[i:]}')
                return PART1_POINT_VALUES[c]
    return 0



def part_1(lines):
    total_score = 0
    for line in lines:
        open_stack = deque()
        for i, c in enumerate(line):
            if c in OPENERS:
                open_stack.append(c)
            elif c in CLOSERS:
                last_opener = open_stack.pop()
                if last_opener != MATCHING_OPENING_CHARACTERS[c]:
                    print(f'{c} does not match. Line {line[:i]}   {line[i:]}')
                    total_score += PART1_POINT_VALUES[c]

    print(f'part 1: {total_score}')

def part_2(lines):
    line_scores = []
    for line in lines:
        line_score = 0
        open_stack = deque()
        corrupted = False
        for i, c in enumerate(line):
            if c in OPENERS:
                open_stack.append(c)
            elif c in CLOSERS:
                last_opener = open_stack.pop()
                if last_opener != MATCHING_OPENING_CHARACTERS[c]:
                    corrupted = True
                    break
        score = 0
        if not corrupted:
            while len(open_stack) > 0:
                line_score = line_score*5 + PART2_POINT_VALUES[ MATCHING_CLOSING_CHARACTERS[open_stack.pop()]]
            line_scores.append(line_score)
    print(f'part 2: {np.median(np.array(line_scores))}')


if __name__ == '__main__':
    with open('day10_input.txt') as f:
        lines = f.readlines()
    # part_1(lines)
    part_2(lines)
