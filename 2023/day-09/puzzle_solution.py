import numpy as np

from shared.file_handling import get_file_strings


input_sequences = get_file_strings('official_input.txt')
int_sequences = []
for sequence in input_sequences:
    int_sequences.append([int(value.strip()) for value in sequence.split(" ")])


# Rather than polynomial fitting, which turned out to be too imprecise at high-degree polynomials,
#   ended up just working backwards from the 0-list case and progressively adding the next term up.
#   It's a shame about the polynomial, but it makes sense - fitting 20th degree with 20 points TECHNICALLY works,
#   but is potentially unstable.
def process_sequence(line_sequence: list[int]):
    if sum(value != 0 for value in line_sequence) == 0:
        return 0
    new_sequence = []
    for i in range(0, len(line_sequence)-1):
        new_sequence.append(line_sequence[i+1]-line_sequence[i])
    return line_sequence[-1] + process_sequence(new_sequence)


# Part 1 solution - had to start from scratch after polynomial fitting was too imprecise :(
print(f"Sum of the next values in each sequence: {sum(process_sequence(i) for i in int_sequences)}")

# Part 2 solution - just reversed with a clever little list trick, now the last character is the "first" from part 1
print(f"Sum of the previous values in each sequence: {sum(process_sequence(i[::-1]) for i in int_sequences)}")
