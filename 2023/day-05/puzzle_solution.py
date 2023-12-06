from dataclasses import dataclass
from typing import Iterator

from shared.file_handling import get_file_strings


Seeds = list[int]
ValueRange = tuple[int, int]  # start, end+1

# These are part of the super-inefficient method I came up with
# ----------------------------------------------------------------
def parse_number_list(number_string: str) -> list[int | None]:
    raw_list = number_string.split(" ")
    number_list = [int(raw_number) for raw_number in raw_list if raw_number != '']
    return number_list


def parse_input_map(map_input_file: str) -> dict:
    map_dicts = {}
    with open(map_input_file) as map_file:
        line_number = 0
        current_map = ''
        for line in map_file:
            clean_line = line.strip()
            if line_number == 0:  # Custom handling for the seed list
                seeds_text = clean_line.split(": ")
                seeds_list = parse_number_list(seeds_text[1])
                map_dicts["source_seeds"] = seeds_list
                line_number += 1
            else:
                if clean_line.__contains__("map"):
                    type_split = clean_line.split(" ")
                    current_map = type_split[0]
                    map_dicts[current_map] = {}
                elif clean_line == '':
                    pass  # line break in the input file
                else:
                    line_details = parse_number_list(clean_line)
                    dest_start = line_details[0]
                    source_start = line_details[1]
                    range_length = line_details[2]
                    # print(f"current_map: {current_map}, "
                    #       f"dest_start: {dest_start}, "
                    #       f"source_start: {source_start}, "
                    #       f"range_length: {range_length}")
                    for i in range(0, range_length):
                        map_dicts[current_map][source_start+i] = dest_start+i
    # for k, v in map_dicts.items():
    #     print(f"{k}, {v}")
    return map_dicts


@dataclass
class CategoryMap:
    category_name: str
    next_category: str
    map_tuples: list[tuple[int, int, int]]

    def apply(self, value: int) -> int:
        for to_id, from_id, length in self.map_tuples:
            if from_id <= value < from_id + length:
                return to_id + (value - from_id)
        return value


def parse_map_line(line: str) -> tuple[str, str]:
    from_category, to_category = line.replace(" map:", "").split("-to-")
    return from_category, to_category


def parse_map_tuples(line_iterator: Iterator[str]):
    category_map_tuples: list[tuple[int, int, int]] = []
    while True:
        try:
            line = next(line_iterator)
        except StopIteration:
            break

        if line == "":
            break

        to_id, from_id, length = line.split(" ")
        category_map_tuples.append((int(to_id), int(from_id), int(length)))

    return category_map_tuples


def parse_lines_efficient(lines: list[str]) -> tuple[Seeds, dict[str, CategoryMap]]:
    line_iterator = iter(lines)
    seed_line = next(line_iterator)
    seeds = [int(n) for n in seed_line.replace("seeds: ", "").split(" ")]

    category_maps: dict[str, CategoryMap] = {}

    while True:
        try:
            line = next(line_iterator)
        except StopIteration:
            break

        if "map" in line:
            from_category, to_category = parse_map_line(line)
            map_tuples = parse_map_tuples(line_iterator)

            category_map = CategoryMap(from_category, to_category, map_tuples)
            category_maps[from_category] = category_map

    return seeds, category_maps


def get_location_from_seed(seed_number: int, category_maps: dict[str, CategoryMap]) -> int:
    category = "seed"
    value = seed_number
    while category != "location":
        category_map = category_maps[category]
        value = category_map.apply(value)
        category = category_map.next_category
    return value


def apply_category_map_to_range(category_map: CategoryMap, value_range: ValueRange) -> list[ValueRange]:

    all_starts = [from_id for _, from_id, _ in category_map.map_tuples]
    all_ends = [from_id + length for _, from_id, length in category_map.map_tuples]
    all_s_and_t = sorted(set(all_starts + all_ends))

    split_ranges = []
    next_start = value_range[0]
    for v in all_s_and_t:
        if v <= value_range[0] or v >= value_range[1]:
            continue
        split_ranges.append((next_start, v))
        next_start = v
    split_ranges.append((next_start, value_range[1]))

    new_ranges = []
    for s, t in split_ranges:
        new_start = category_map.apply(s)
        new_end = new_start + (t - s)
        new_ranges.append((new_start, new_end))

    return new_ranges


def get_location_from_seed_intervals(seed_intervals: list[ValueRange],
                                     category_maps: dict[str, CategoryMap]) -> list[ValueRange]:
    category = "seed"
    intervals = seed_intervals
    while category != "location":
        category_map = category_maps[category]
        all_new_intervals = []
        for interval in intervals:
            new_intervals = apply_category_map_to_range(category_map, interval)
            all_new_intervals.extend(new_intervals)

        intervals = all_new_intervals
        category = category_map.next_category

    return intervals



if __name__ == '__main__':

    # Define the input file
    input_file = 'official_input.txt'

    # I cannot take credit for discovering this solution, but since it uses a methodology I have never seen in
    #  the Python language I am perfectly comfortable using it, learning the new components, and giving credit
    #   where credit is due - Bernd Prach on YouTube https://www.youtube.com/watch?v=BBbHZpDbKas
    file_lines = get_file_strings(input_file)

    seeds, category_maps = parse_lines_efficient(file_lines)

    seed_to_location = {}
    for seed in seeds:
        location = get_location_from_seed(seed, category_maps)
        seed_to_location[seed] = location

    min_location = min(seed_to_location.values())
    print(f"The minimum location for the given seeds is: {min_location}")

    seeds_long, category_maps_long = parse_lines_efficient(file_lines)
    seed_intervals = []
    for i in range(len(seeds_long) // 2):
        s = seeds_long[2*i]
        length = seeds_long[2*i+1]
        seed_intervals.append((s, s+length))

    location_intervals = get_location_from_seed_intervals(seed_intervals, category_maps_long)
    min_location_long = min(i[0] for i in location_intervals)
    print(f"The minimum location for the given seeds ranges is: {min_location_long}")

    # This solution is NOT memory-efficient (my laptop crashes out with memory error)
    # --------------------------------------------------------------------------------
    # Parse out the input file into a dict of dicts to provide efficient 1-1 lookups
    if input_file == "test.txt":
        mapping_dicts = parse_input_map(input_file)

        print()
        for seed in mapping_dicts['source_seeds']:
            result_value = -1
            print(f"Seed - {seed}")
            for map_string, values in mapping_dicts.items():
                if map_string != 'source_seeds':
                    if result_value == -1:
                        try:
                            result_value = values[seed]
                        except KeyError:
                            result_value = seed
                        print(f"{map_string}: {result_value}")
                    else:
                        try:
                            result_value = values[result_value]
                            print(f"{map_string}: {result_value}")
                        except KeyError:
                            result_value = result_value
                            print(f"{map_string}: {result_value}")
            print(f"Seed: {seed}  -  Location: {result_value}\n")
    else:
        print("\n\nOLD METHOD SKIPPED\nNot going to try this on the full data set, goes kaput!")
