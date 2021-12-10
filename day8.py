"""
--- Day 8: Seven Segment Search ---
You barely reach the safety of the cave when the whale smashes into the cave mouth, collapsing it. Sensors indicate another exit to this cave at a much greater depth, so you have no choice but to press on.

As your submarine slowly makes its way through the cave system, you notice that the four-digit seven-segment displays in your submarine are malfunctioning; they must have been damaged during the escape. You'll be in a lot of trouble without them, so you'd better figure out what's wrong.

Each digit of a seven-segment display is rendered by turning on or off any of seven segments named a through g:

  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
So, to render a 1, only segments c and f would be turned on; the rest would be off. To render a 7, only segments a, c, and f would be turned on.

The problem is that the signals which control the segments have been mixed up on each display. The submarine is still trying to display numbers by producing output on signal wires a through g, but those wires are connected to segments randomly. Worse, the wire/segment connections are mixed up separately for each four-digit display! (All of the digits within a display use the same connections, though.)

So, you might know that only signal wires b and g are turned on, but that doesn't mean segments b and g are turned on: the only digit that uses two segments is 1, so it must mean segments c and f are meant to be on. With just that information, you still can't tell which wire (b/g) goes to which segment (c/f). For that, you'll need to collect more information.

For each display, you watch the changing signals for a while, make a note of all ten unique signal patterns you see, and then write down a single four digit output value (your puzzle input). Using the signal patterns, you should be able to work out which pattern corresponds to which digit.

For example, here is what you might see in a single entry in your notes:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
cdfeb fcadb cdfeb cdbaf
(The entry is wrapped here to two lines so it fits; in your notes, it will all be on a single line.)

Each entry consists of ten unique signal patterns, a | delimiter, and finally the four digit output value. Within an entry, the same wire/segment connections are used (but you don't know what the connections actually are). The unique signal patterns correspond to the ten different ways the submarine tries to render a digit using the current wire/segment connections. Because 7 is the only digit that uses three segments, dab in the above example means that to render a 7, signal lines d, a, and b are on. Because 4 is the only digit that uses four segments, eafb means that to render a 4, signal lines e, a, f, and b are on.

Using this information, you should be able to work out which combination of signal wires corresponds to each of the ten digits. Then, you can decode the four digit output value. Unfortunately, in the above example, all of the digits in the output value (cdfeb fcadb cdfeb cdbaf) use five segments and are more difficult to deduce.

For now, focus on the easy digits. Consider this larger example:

be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb |
fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec |
fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |
cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |
efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |
gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |
gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |
cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |
ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |
gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |
fgae cfgab fg bagce
Because the digits 1, 4, 7, and 8 each use a unique number of segments, you should be able to tell which combinations of signals correspond to those digits. Counting only digits in the output values (the part after | on each line), in the above example, there are 26 instances of digits that use a unique number of segments (highlighted above).

In the output values, how many times do digits 1, 4, 7, or 8 appear?

------- PART 2 ---------------------
For each entry, determine all of the wire/segment connections and decode the four-digit output values.
What do you get if you add up all of the output values?
"""
from collections import Counter

def create_encoder(signal_patterns):
    """ Create an encoding for each segment letter.
    Count the frequency of each letter in the 10 scrambled signals. Encode letter as 10^(letter_frequency-3)  """
    character_counts = Counter(signal_patterns)
    least_common = min(character_counts.values())
    encoder = {letter: (letter_frequency-least_common) for letter, letter_frequency in character_counts.items()}
    return encoder


def encode_digit_output(digit_output, encoder):
    """ Apply encoder to encode the digit output string as a number which encodes the number of occurrences of
    each character frequency type + the number of segments in the digit """
    encoding = 0
    # return len(digit_output)
    for letter in digit_output:
        encoding += 10**(encoder[letter]+1)
    encoding = encoding + len(digit_output)
    return encoding


def create_decoder(encoder):
    """ Apply encoder to the unscrambled "regular" digit segment string to create a decoder.
    Maps encoded digit segment string to the numeric digit it represents """
    return {encode_digit_output(value, encoder): key for key, value in SEGMENTS_IN_DIGITS.items()}


def determine_digits_in_line(signal_patterns, digit_outputs, decoder):
    encoder = create_encoder(signal_patterns.replace(' ', ''))
    # decoder = create_decoder(encoder)
    encoded_digit_outputs = [encode_digit_output(x, encoder) for x in digit_outputs]
    decoded_digits = []
    for encoded_digit in encoded_digit_outputs:
        decoded_digit = decoder[encoded_digit]
        decoded_digits.append(decoded_digit)
    # decoded_digits = [decoder[x] for x in encoded_digit_outputs]
    return decoded_digits


def parse_input_line(line):
    line = line.replace('\n', '')
    signal_patterns, digit_outputs = line.split(' | ')
    # signal_patterns = signal_patterns.split(' ')
    digit_outputs = digit_outputs.split(' ')
    return (signal_patterns, digit_outputs)


def part_1(decoded_outputs):
    flattened_decoded_outputs = []
    [flattened_decoded_outputs.extend(x) for x in decoded_outputs]
    digit_counts = Counter(flattened_decoded_outputs)
    answer = digit_counts[1] + digit_counts[4] + digit_counts[7] + digit_counts[8]
    print(f'answer to part 1 is: {answer}')


def part_2(decoded_outputs):
    total = 0
    for decoded_output in decoded_outputs:
        output_value = 0
        for i, val in enumerate(decoded_output):
            output_value += val * 10**(3-i)
        total += output_value
    print(f'answer to part 2 is: {total}')
    return total

SEGMENTS_IN_DIGITS = {0: 'abcefg',
                      1: 'cf',
                      2: 'acdeg',
                      3: 'acdfg',
                      4: 'bcdf',
                      5: 'abdfg',
                      6: 'abdefg',
                      7: 'acf',
                      8: 'abcdefg',
                      9: 'abcdfg'
                      }

if __name__ == '__main__':
    with open('day8_input.txt') as f:
        lines = f.readlines()

    # tests
    digit_list = list(range(10))
    nonscrambled_signal_patterns = ' '.join([SEGMENTS_IN_DIGITS[x] for x in digit_list])
    decoder = create_decoder(create_encoder(nonscrambled_signal_patterns))
    nonscrambled_digit_outputs = [SEGMENTS_IN_DIGITS[x] for x in digit_list]
    decoded_digit_outputs = determine_digits_in_line(nonscrambled_signal_patterns, nonscrambled_digit_outputs, decoder)
    print(decoded_digit_outputs)
    # assert digit_list == decoded_digit_outputs



    # solve puzzle
    puzzle_input = [parse_input_line(line) for line in lines]
    decoded_outputs = []
    for signal_patterns, digit_outputs in puzzle_input:
        # print(signal_patterns)
        # print(digit_outputs)
        decoded_output = determine_digits_in_line(signal_patterns=signal_patterns, digit_outputs=digit_outputs, decoder=decoder)
        decoded_outputs.append(decoded_output)
    part_1(decoded_outputs)
    part_2(decoded_outputs)