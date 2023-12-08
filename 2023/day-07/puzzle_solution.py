from collections import Counter

from shared.file_handling import get_file_strings


# Sorting rules:
#   1) Five-of-a-kind [AAAAA]
#   2) Four-of-a-kind [AAAAK]
#   3) Full house [AAAKK] (three-of-a-kind + pair)
#   4) Three-of-a-kind [AAAK2]
#   5) Two-Pair [22334]
#   6) One Pair [22345]
#   7) High card [23456]
# Then...
#   If rules are the same, check first card in original hand, then second, then third, and so on
#   I don't think it'll happen, but raise an exception on a perfect tie
# Individual card ranks (Ace high):
#  A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2
SORT_ORDER = '23456789TJQKA'
JOKER_ORDER = 'J23456789TQKA'  # This is used for the solution to part 2

# Create a mapping from character to its order
char_order_map = {char: index for index, char in enumerate(SORT_ORDER)}
default_order = len(SORT_ORDER)  # Default order for characters not in custom char list
joker_order_map = {char: index for index, char in enumerate(JOKER_ORDER)}
joker_default = len(JOKER_ORDER)  # Default order for characters not in custom char list


# Custom sorting function for strings
def compare_keys(key1, key2):
    for c1, c2 in zip(key1, key2):
        if char_order_map.get(c1, default_order) != char_order_map.get(c2, default_order):
            return char_order_map.get(c1, default_order) - char_order_map.get(c2, default_order)
    return len(key1) - len(key2)  # If all characters are equal, shorter string comes first


def parse_file(input_strings: list[str]) -> dict[str, dict[str, str]]:
    game_dict = {}
    for line in input_strings:
        clean_line = line.strip().split(" ")
        game_dict[str(clean_line[0])] = {
            "original_hand": str(clean_line[0]),
            "bid": int(clean_line[1])
        }
    return game_dict


def count_original_hands(game_dict: dict) -> dict[int, dict]:
    for key, game_values in game_dict.items():
        this_hand = game_values["original_hand"]
        counts = Counter(this_hand)
        matches = {count: [] for count in [2, 3, 4, 5]}
        for char, count in counts.items():
            if count > 1:
                matches[count].append(char)
        formatted_matches = {k: v for k, v in matches.items() if v}
        game_dict[key]['counts'] = formatted_matches

    return game_dict


def count_joker_hands(game_dict: dict) -> dict[int, dict]:

    return game_dict


def group_results(game_dict: dict) -> dict[str, dict]:
    grouped_games = {}
    five_of_a_kind = {}
    four_of_a_kind = {}
    full_house = {}
    three_of_a_kind = {}
    two_pair = {}
    one_pair = {}
    high_card = {}
    for key, game in game_dict.items():
        this_hand = {key: game}
        count_keys = game['counts'].keys()

        # Five-of-a-kind condition: len(counts) == 1 and 5 in count_keys
        if len(game['counts']) == 1 and (5 in count_keys):
            five_of_a_kind[key] = this_hand

        # Four-of-a-kind condition: len(counts) == 1 and 4 in count_keys
        elif (len(game['counts']) == 1) and (4 in count_keys):
            four_of_a_kind[key] = this_hand

        # Full House condition: len(counts) == 2 and 2, 3 both on count_keys
        elif (len(game['counts']) == 2) and (2 in count_keys) and (3 in count_keys):
            full_house[key] = this_hand

        # Three-of-a-kind condition: len(counts) == 1 and 3 in count_keys
        elif (len(game['counts']) == 1) and (3 in count_keys):
            three_of_a_kind[key] = this_hand

        # Two-pair conditions: len(counts) == 1 and 2 in count_keys
        elif (len(game['counts']) == 1) and (2 in count_keys) and (len(game['counts'][2]) > 1):
            two_pair[key] = this_hand

        # One-pair conditions: len(counts) == 1 and 2 in count_keys and len(counts[2]) == 1
        elif (len(game['counts']) == 1) and (2 in count_keys) and (len(game['counts'][2]) == 1):
            one_pair[key] = this_hand

        else:
            high_card[key] = this_hand

        grouped_games['high_card'] = high_card
        grouped_games['one_pair'] = one_pair
        grouped_games['two_pair'] = two_pair
        grouped_games['three_of_a_kind'] = three_of_a_kind
        grouped_games['full_house'] = full_house
        grouped_games['four_of_a_kind'] = four_of_a_kind
        grouped_games['five_of_a_kind'] = five_of_a_kind

    return grouped_games


def rank_games(grouped_games: dict) -> dict:
    ranked_games = {}
    rank = 1
    for key, group in grouped_games.items():
        if len(group.values()) > 1:
            # Sort the keys of your_dict by custom character order
            sorted_keys = sorted(group.keys(), key=lambda k: [char_order_map.get(c, default_order) for c in k])

            # Create an OrderedDict with sorted keys
            ordered_dict = {}
            for i in sorted_keys:
                ordered_dict[i] = group[i]
            for game in ordered_dict.values():
                ranked_games[rank] = game
                rank += 1
        else:
            for game_entry in group.values():
                ranked_games[rank] = game_entry
                rank += 1

    return ranked_games


def calculate_game_winnings(games_with_ranks: dict) -> int:
    running_winnings = 0
    for rank, game in games_with_ranks.items():
        for key in game.keys():
            bid_value = game[key]['bid']
            running_winnings += bid_value * rank

    return running_winnings


if __name__ == '__main__':

    # Define the input file and read it into memory
    input_file = 'official_input.txt'
    line_strings = get_file_strings(input_file)

    initial_data = parse_file(line_strings)
    counted_hands = count_original_hands(initial_data)
    game_groups = group_results(counted_hands)
    games_by_rank = rank_games(game_groups)

    # Part 1 solution
    game_winnings = calculate_game_winnings(games_by_rank)
    print(game_winnings)

    # Part 2 solution - J is now Joker, not Jack
    # For the purposes of determining what kind of hand it is, Joker is whatever makes the hand highest type
    # For the purposes of determining rank thereafter, the Joker is the lowest position in sort order
    #       Need to tweak group_results logic to account for Joker support
    #       Need to tweak rank_games logic to allow for a configurable sort order
    joker_counted_hands = count_joker_hands(initial_data)
