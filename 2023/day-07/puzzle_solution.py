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
SORT_ORDER = '23456789TJQKA'  # This is used for the solution to part 1
JOKER_ORDER = 'J23456789TQKA'  # This is used for the solution to part 2


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
    for key, game_values in game_dict.items():
        this_hand = game_values["original_hand"]
        counts = Counter(this_hand)
        all_matches = {count: [] for count in [1, 2, 3, 4, 5]}
        for char, count in counts.items():
            if count >= 1:
                all_matches[count].append(char)
        formatted_joker_matches = {k: v for k, v in all_matches.items() if v}
        # At this point we've got a dict of {count: [chars], ...}
        joker_count = 0
        for count, char_list in formatted_joker_matches.items():
            if "J" in char_list:
                joker_count += count
                char_list.remove("J")
        game_dict[key]['joker_count'] = joker_count

        game_dict[key]['counts'] = formatted_joker_matches
    return game_dict


def label_hand(counts, count_by_keys, current_hand, use_jokers=False):
    if use_jokers:
        game_details = next(iter(current_hand.values()))
        joker_count = game_details['joker_count']
        if joker_count > 0:  # we now only need to worry about the case of having at least 1 Joker card
            match joker_count:
                case 5: return "five-of-a-kind"
                case 4: return "four-of-a-kind"
                case 3:
                    if 2 in count_by_keys:
                        return "five-of-a-kind"
                    else:
                        return "four-of-a-kind"
                case 2:
                    if 3 in count_by_keys:
                        return "five-of-a-kind"
                    elif 2 in count_by_keys:
                        return "four-of-a-kind"
                    else:
                        return "three-of-a-kind"
                case 1:
                    if 4 in count_by_keys:
                        return "five-of-a-kind"
                    elif 3 in count_by_keys:
                        return "four-of-a-kind"
                    elif 2 in count_by_keys:
                        return "three-of-a-kind"
                    else:
                        return "one-pair"

    # Common logic for both cases (use_jokers True or False)
    if len(counts) == 1:
        if 5 in count_by_keys:
            return "five-of-a-kind"
        elif 4 in count_by_keys:
            return "four-of-a-kind"
        elif 3 in count_by_keys:
            return "three-of-a-kind"
        elif 2 in count_by_keys:
            # Check the number of pairs for two-pair and one-pair
            pair_count = len(counts[2])
            if pair_count > 1:
                return "two-pair"
            elif pair_count == 1:
                return "one-pair"
    elif len(counts) == 2 and 2 in count_by_keys and 3 in count_by_keys:
        return "full-house"

    return "high-card"


def group_results(game_dict: dict, use_jokers=False) -> dict[str, dict]:
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
        hand_label = label_hand(game['counts'], count_keys, this_hand, use_jokers=use_jokers)
        match hand_label:
            case "five-of-a-kind":
                five_of_a_kind[key] = this_hand
            case "four-of-a-kind":
                four_of_a_kind[key] = this_hand
            case "full-house":
                full_house[key] = this_hand
            case "three-of-a-kind":
                three_of_a_kind[key] = this_hand
            case "two-pair":
                two_pair[key] = this_hand
            case "one-pair":
                one_pair[key] = this_hand
            case "high-card":
                high_card[key] = this_hand
            case _:
                print("UNKNOWN RESULT RETURNED, DEBUG THIS")

        grouped_games['high_card'] = high_card
        grouped_games['one_pair'] = one_pair
        grouped_games['two_pair'] = two_pair
        grouped_games['three_of_a_kind'] = three_of_a_kind
        grouped_games['full_house'] = full_house
        grouped_games['four_of_a_kind'] = four_of_a_kind
        grouped_games['five_of_a_kind'] = five_of_a_kind

    return grouped_games


def rank_games(grouped_games: dict, use_jokers=False) -> dict:
    # Create a mapping from character to its order
    char_order_map = {char: index for index, char in enumerate(SORT_ORDER)}
    default_order = len(SORT_ORDER)  # Default order for characters not in custom char list
    joker_order_map = {char: index for index, char in enumerate(JOKER_ORDER)}
    joker_default = len(JOKER_ORDER)  # Default order for characters not in custom char list

    ranked_games = {}
    rank = 1
    for key, group in grouped_games.items():
        if len(group.values()) > 1:
            # Sort the keys of your_dict by custom character order
            if use_jokers:
                sorted_keys = sorted(group.keys(), key=lambda k: [joker_order_map.get(c, joker_default) for c in k])
            else:
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
    #   A result of 250254244 is correct
    game_winnings = calculate_game_winnings(games_by_rank)
    print(game_winnings)

    # Part 2 solution - J is now Joker, not Jack
    # For the purposes of determining what kind of hand it is, Joker is whatever makes the hand highest type
    # For the purposes of determining rank thereafter, the Joker is the lowest position in sort order
    #       Need to tweak group_results logic to account for Joker support
    #       Need to tweak rank_games logic to allow for a configurable sort order
    joker_counted_hands = count_joker_hands(initial_data)
    joker_game_groups = group_results(joker_counted_hands, use_jokers=True)
    joker_games_by_rank = rank_games(joker_game_groups, use_jokers=True)

    # Part 2 solution
    #   A result of 252956851 is too high, need to debug further -> forgot to rework ranking to use Jokers
    #   A result of 252663288 is still too high, need to debug further -> ?????
    joker_game_winnings = calculate_game_winnings(joker_games_by_rank)
    print(joker_game_winnings)

