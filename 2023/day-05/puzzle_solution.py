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


if __name__ == '__main__':

    # Define the input file
    input_file = 'official_input.txt'

    # Parse out the input file into a dict of dicts to provide efficient 1-1 lookups
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
