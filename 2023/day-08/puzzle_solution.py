import math
import time

from shared.file_handling import get_file_strings

# ---------------------------------------------------------------------------------------
# Get first line as input for directions through puzzle
# For each line thereafter, do the following:
#   Add entry to decision_dict(start: str, dict{L: str, R: str})
#       Get first set of 3 characters, "start"
#       Get second set of 3 characters, "L"
#       Get third set of 3 characters, "R"
# Once the file is read, start "walking":
#   Get starting point (initialize to first line found)
#   Initialize step count to 0
#   Loop Start
#   Determine next step to take (L/R)
#       If at the end of the line, loop back to first (LR -> LRLRLRLRLRLR...)
#   Get destination
#       If destination == ZZZ, increment step count and break
#       Else increment step count and set destination as new starting point
#   Loop
# ---------------------------------------------------------------------------------------
input_strings = get_file_strings("official_input.txt")
decision_dict = {}
steps = []

for line in input_strings:
    if not line.__contains__("=") and line != '':
        cleaned_line = line.strip()
        steps = [character for character in cleaned_line]  # Sets the steps to follow on a loop
    elif line.__contains__("="):
        cleaned_line = line.replace(" = (", ",").replace(", ", ",").replace(")", "")
        split_line = cleaned_line.split(",")
        decision_dict[split_line[0]] = {"L": split_line[1], "R": split_line[2]}

step_count = 0
step_index = 0
stage = 'AAA'
initial_time = time.perf_counter()
while True:
    step_count += 1
    if step_index >= len(steps):
        step_index = 0
    direction = steps[step_index]
    step_index += 1

    next_stage = decision_dict[stage][direction]
    if next_stage == "ZZZ":
        break
    else:
        stage = next_stage

ending_time = time.perf_counter()
print(f"ZZZ reached in {step_count} steps and taking {(ending_time - initial_time):.6f} seconds")
# The correct answer was 16697

ends_with_a = {}
a_step_counts = []
for this_stage in decision_dict.keys():
    if this_stage[2] == "A":
        ends_with_a[this_stage] = 0
a_initial_time = time.perf_counter()
for a_stage in ends_with_a.keys():
    a_step_count = 0
    a_step_index = 0
    while True:
        a_step_count += 1
        if a_step_index >= len(steps):
            a_step_index = 0
        direction = steps[a_step_index]
        a_step_index += 1

        a_next_stage = decision_dict[a_stage][direction]
        if a_next_stage[2] == "Z":
            break
        else:
            a_stage = a_next_stage
    a_step_counts.append(a_step_count)


def lcm_of_list(numbers):
    """Calculate the LCM of a list of integers."""
    if not numbers:
        return 0
    lcm_result = numbers[0]
    for number in numbers[1:]:
        lcm_result = math.lcm(lcm_result, number)
    return lcm_result


lcm_of_a_list = lcm_of_list(a_step_counts)
a_end_time = time.perf_counter()
print(f"All endings in Z reached in {lcm_of_a_list} steps and taking {(a_end_time - a_initial_time):.6f} seconds")
# The correct answer was 10668805667831
# So what the heck does the LCM have to do with this?  Graph theory - will need significant time to understand the WHY
