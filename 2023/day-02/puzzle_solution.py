import math


def get_game_id(raw_game_string: str) -> int:
    return int(raw_game_string.split(" ")[1])


def get_play_color(play_color_input: str) -> str:
    raw_color_result = str(play_color_input.split(" ")[1])
    if raw_color_result.__contains__(";"):
        color_result = raw_color_result[:-1]
        color_result = color_result.strip()
    else:
        color_result = raw_color_result.strip()
    return color_result


def get_play_color_count(color_entry_input: str) -> int:
    return int(color_entry_input.split(" ")[0])


def get_game_details(raw_details_string: str) -> dict:
    details_summary = dict()
    play_split = raw_details_string.split("; ")
    for entry in play_split:
        color_split = entry.split(", ")
        for color_entry in color_split:
            color_id = get_play_color(color_entry)
            color_value = get_play_color_count(color_entry)
            try:
                existing_data = details_summary[color_id]
                existing_min = existing_data[0]
                existing_max = existing_data[1]
                # If result is greater than existing max, set new max
                if color_value >= existing_max:
                    if existing_min == 0:
                        details_summary[color_id] = (existing_max, color_value)
                    else:
                        details_summary[color_id] = (existing_min, color_value)
                # If result is between existing min and max and min = 0, set new min
                elif ((color_value < existing_max)
                      and (color_value > existing_min)
                      and (existing_min == 0)):
                    details_summary[color_id] = (color_value, existing_max)
                # If result is less than existing min, set new min
                elif color_value < existing_min:
                    details_summary[color_id] = (color_value, existing_max)
            except KeyError:
                details_summary[color_id] = (0, color_value)
    print(details_summary)

    return details_summary


def get_game_summary(data_file: str) -> dict:
    games_summary = {}
    with open(data_file) as f:
        for line in f.readlines():
            line_clean = line.strip()
            # Get the game id for the line
            game_results_split = line_clean.split(": ")
            # Game ID can be pulled from the first list element, color details from the second
            game_id = get_game_id(game_results_split[0])
            game_details = get_game_details(game_results_split[1])
            games_summary[game_id] = game_details
    return games_summary


def check_color(game_color_bounds, check_count: int) -> bool:
    lower_bound = game_color_bounds[0]
    upper_bound = game_color_bounds[1]

    if upper_bound <= check_count:
        return True
    else:
        return False


def get_plausible_games(games_played: dict, check_counts: dict) -> list[int]:
    potential_games = []
    for game_id, game_detes in games_played.items():
        if (check_color(game_detes['red'], check_counts['red'])
                and check_color(game_detes['green'], check_counts['green'])
                and check_color(game_detes['blue'], check_counts['blue'])):
            potential_games.append(int(game_id))
    return potential_games


def get_game_powers(games_played: dict):
    powers_list = []
    for game_id, game_detes in games_played.items():
        initial_power = 1
        for color_value in game_detes.values():
            initial_power *= color_value[1]
        powers_list.append(initial_power)

    return powers_list


if __name__ == '__main__':
    # input_file = 'test_001.txt'
    # input_file = 'debugger.txt'
    input_file = 'aoc_official_input_file.txt'

    # Conditions for plausibility check:
    conditions = {
        "red": 12,
        "green": 13,
        "blue": 14
    }

    game_inputs = get_game_summary(input_file)
    plausible_games = get_plausible_games(game_inputs, conditions)
    sum_of_plausible_game_ids = math.fsum(plausible_games)
    print(f"Sum of plausible game ids: {int(sum_of_plausible_game_ids)}")

    game_powers = get_game_powers(game_inputs)
    print(f"Sum of game powers: {int(math.fsum(game_powers))}")
