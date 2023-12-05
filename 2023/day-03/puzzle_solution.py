def get_puzzle_dimensions(input_file: str) -> tuple:
    with open(input_file) as f:
        row_count = 0
        column_count = 0
        column_counts = []
        for line in f:
            row_count += 1
            clean_line = line.strip('\n')
            column_counts.append(len(clean_line))

        # If all rows have same column length, return the single value, else return a list
        column_set = set(column_counts)
        if len(column_set) == 1:
            return row_count, column_counts[0]
        else:
            return row_count, column_counts


def get_puzzle_symbol_locations(puzzle_file: str, n_rows: int, n_columns: int) -> dict:
    symbol_dict = {}
    with open(puzzle_file) as f:
        row_index = 0
        for line in f:
            col_index = 0
            while col_index < n_columns:
                clean_line = line.strip()
                for character in clean_line:
                    if not character.isalnum() and character != '.':
                        symbol_string = f"{character}.{row_index}.{col_index}"
                        symbol_dict[symbol_string] = {"row": row_index, "col": col_index}
                    col_index += 1
            row_index += 1

    return symbol_dict


def get_puzzle_number_locations(puzzle_file: str, n_rows: int, n_cols: int) -> dict:
    numbers_dict = {}
    with open(puzzle_file) as f:
        row_index = 0
        start_index = 0
        end_index = 0

        for line in f:
            col_index = 0
            check_string = ''
            while col_index < n_cols:
                clean_line = line.strip()
                for character in clean_line:
                    if character.isnumeric():
                        if check_string == '':
                            start_index = col_index
                        check_string += character
                    if character == '.' or not character.isnumeric():
                        if check_string != '':
                            end_index = col_index - 1
                            numbers_dict[
                                f"{check_string}.{row_index}.{start_index}.{end_index}"
                            ] = {
                                "value": int(check_string),
                                "row": int(row_index),
                                "start_index": int(start_index),
                                "end_index": int(end_index),
                                "flagged": False
                            }
                            check_string = ''
                    col_index += 1
                if check_string != '':
                    numbers_dict[
                        f"{check_string}.{row_index}.{start_index}.{col_index}"
                    ] = {
                        "value": int(check_string),
                        "row": int(row_index),
                        "start_index": int(start_index),
                        "end_index": int(col_index),
                        "flagged": False
                    }
            row_index += 1

    return numbers_dict


def flag_important_numbers(symbols_results: dict, numbers_results: dict, n_rows: int, n_cols: int) -> dict:
    for key, number_info in numbers_results.items():
        # For each number, run a lookup against the symbols and set the
        # flagged value to True if in the adjacent points in the grid there is a symbol
        number_row = number_info["row"]
        number_start = number_info["start_index"]
        number_end = number_info["end_index"]
        for symbol_info in symbols_results.values():
            symbol_row = symbol_info["row"]
            symbol_col = symbol_info["col"]
            row_check = (max(0, number_row-1) <= symbol_row <= min(n_rows, number_row+1))
            col_check = (max(0, number_start-1) <= symbol_col <= min(n_cols, number_end+1))
            if row_check and col_check:
                numbers_results[key]["flagged"] = True
    return numbers_results


def get_puzzle_labeled_sum(numbers_dict: dict) -> int:
    my_sum = 0
    values_list = []
    for num_v in numbers_dict.values():
        if num_v["flagged"]:
            values_list.append(num_v["value"])

    print(values_list)

    for num in values_list:
        my_sum += num

    return my_sum


def get_gear_info(gear_input_file: str, n_columns: tuple) -> dict:
    gear_info = {}
    with open(gear_input_file) as gear_file:
        # iterate through the file and pick out symbols only matching "*" character
        row_index = 0
        for line in gear_file:
            col_index = 0
            while col_index < n_columns[1]:
                clean_line = line.strip()
                for character in clean_line:
                    if character == '*':
                        symbol_string = f"{character}.{row_index}.{col_index}"
                        gear_info[symbol_string] = {"row": row_index, "col": col_index, "count": 0, "nums": []}
                    col_index += 1
            row_index += 1
    return gear_info


def count_gear_numbers(gear_dict: dict, numbers_dict: dict, n_rows: int, n_cols: int) -> dict:
    for key, gear in gear_dict.items():
        gear_row = gear["row"]
        gear_col = gear["col"]
        for nkey, number in numbers_dict.items():
            number_value = number["value"]
            number_row = number["row"]
            number_start = number["start_index"]
            number_end = number["end_index"]
            row_check = (max(0, number_row - 1) <= gear_row <= min(n_rows, number_row + 1))
            column_check = (max(0, number_start - 1) <= gear_col <= min(n_cols, number_end + 1))
            if row_check and column_check:
                gear_dict[key]["count"] += 1
                gear_dict[key]["nums"].append(number_value)
    return gear_dict


def get_gear_ratio(counted_gear_input: dict) -> int:
    gear_ratio_sum = 0

    for key, gear_value in counted_gear_input.items():
        gear_count = gear_value["count"]
        gear_list = gear_value["nums"]
        if gear_count == 2:
            my_gear_ratio = int(gear_list[0]) * int(gear_list[1])
            gear_ratio_sum += my_gear_ratio

    return gear_ratio_sum


if __name__ == '__main__':
    # Define the file to be used for execution:
    # input_file = "test_001.txt"
    # input_file = "debugging.txt"
    input_file = "aoc_official_input_file.txt"

    # Get the puzzle dimensions for use in looped reading:
    puzzle_dimens = get_puzzle_dimensions(input_file)

    # Break out if rows have different character lengths:
    if isinstance(puzzle_dimens[1], list):
        print(f"Different character lengths in lines: {puzzle_dimens}")
        exit(0)

    # Get the rectangular coordinates of the symbols in the puzzle
    symbol_lookup = get_puzzle_symbol_locations(input_file,
                                                n_rows=puzzle_dimens[0],
                                                n_columns=puzzle_dimens[1])
    for k, v in symbol_lookup.items():
        print(f"{k}, {v}")
    print("")

    # Get the rectangular coordinates of the numbers in the puzzle
    number_lookup = get_puzzle_number_locations(input_file,
                                                n_rows=puzzle_dimens[0],
                                                n_cols=puzzle_dimens[1])
    for k, v in number_lookup.items():
        print(f"{k}, {v}")
    print("")

    # Label the important numbers
    labeled_numbers = flag_important_numbers(
        symbol_lookup, number_lookup,
        n_rows=puzzle_dimens[0], n_cols=puzzle_dimens[1])
    for k, v in labeled_numbers.items():
        print(f"{k}, {v}")
    print("")

    # Get True labeled sum
    true_sum = get_puzzle_labeled_sum(labeled_numbers)
    print(true_sum)

    # Result of 6313347 is too large, I think there's something in my column-check logic?
    # Result of 6129099 is still too high, so it's not keeping unique values that was the problem
    # Result of 537066 is too low, so there's more than just the symbols between numbers going on
    # Result of 538046 was correct for part 1, was miss-handling the case of a number ending a line

    # ------ PART 2 CODE ------
    gears = get_gear_info(input_file, puzzle_dimens)
    for k, v in gears.items():
        print(f"{k}, {v}")
    print("")

    counted_gears = count_gear_numbers(gears, number_lookup, n_rows=puzzle_dimens[0], n_cols=puzzle_dimens[1])
    for k, v in counted_gears.items():
        print(f"{k}, {v}")
    print("")

    gear_ratio = get_gear_ratio(counted_gears)
    print(gear_ratio)
