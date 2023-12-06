from shared.file_handling import get_file_strings


def parse_line_numbers(split_string: list[str]) -> list[int]:
    return [int(element) for element in split_string if element.isnumeric()]


def parse_line_digits_to_single_number(split_string: list[str]) -> list[int]:
    numerical_elements = [element for element in split_string if element.isnumeric()]
    single_digit = ''.join(str(num_string) for num_string in numerical_elements)
    return [int(single_digit)]


def parse_race_details(input_strings: list[str]) -> dict[int, dict[str, int]]:
    race_dict = {}
    time_numbers = []
    distance_numbers = []

    line_iterator = iter(input_strings)
    while True:
        try:
            line = next(line_iterator)
        except StopIteration:
            break

        if "Time" in line:  # define the time values for each race
            cleaned_line = line.replace("Time: ", "").split(" ")
            # time_numbers = parse_line_numbers(cleaned_line)
            time_numbers = parse_line_digits_to_single_number(cleaned_line)
        if "Distance" in line:  # define the distance values for each race
            cleaned_line = line.replace("Distance: ", "").split(" ")
            # distance_numbers = parse_line_numbers(cleaned_line)
            distance_numbers = parse_line_digits_to_single_number(cleaned_line)

    for i in range(0, len(time_numbers)):
        race_dict[i+1] = {"time": time_numbers[i], "distance": distance_numbers[i]}

    return race_dict


def time_and_distance_check(time_limit: int, distance_limit: int) -> int:
    win_option_count = 0
    for i in range(0, time_limit):
        if i * (time_limit - i) > distance_limit:
            win_option_count += 1
    return win_option_count


def determine_race_options(race_details: dict) -> dict:
    for race_key, race_values in race_details.items():
        race_details[race_key]["win_count"] = time_and_distance_check(race_values["time"], race_values["distance"])
    return race_details


if __name__ == '__main__':

    # Specify which file to use
    file_strings = get_file_strings(input_file_name='official_input.txt')

    race_dictionary = parse_race_details(file_strings)
    labeled_race_dictionary = determine_race_options(race_dictionary)
    for k, v in labeled_race_dictionary.items():
        print(f"{k}, {v}")
    print()

    power_series = 1
    for values in labeled_race_dictionary.values():
        power_series *= values["win_count"]
    print(f"Final result: {power_series}")
