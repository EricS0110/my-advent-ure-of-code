def parse_number_list(number_string: str) -> list[int | None]:
    raw_list = number_string.split(" ")
    number_list = [int(raw_number) for raw_number in raw_list if raw_number != '']
    return number_list


def parse_card_id(card_id_string: str) -> int:
    return int(card_id_string.split(" ")[-1])


def parse_input_file(input_file_name: str) -> dict:
    card_dict = {}
    with open(input_file_name) as infile:
        for line in infile:
            clean_line = line.strip()
            card_split = clean_line.split(": ")
            card_id = parse_card_id(card_split[0])
            card_numbers = card_split[1].split("|")
            winning_numbers = parse_number_list(card_numbers[0])
            playing_numbers = parse_number_list(card_numbers[1])
            card_dict[card_id] = {
                "card_id": int(card_id),
                "winning_numbers": winning_numbers,
                "playing_numbers": playing_numbers,
                "match_count": 0,
                "points_earned": 0
            }
    return card_dict


def count_card_results(cleaned_cards: dict) -> dict:
    for card_id, card_details in cleaned_cards.items():
        winning_numbers = card_details["winning_numbers"]
        playing_numbers = card_details["playing_numbers"]
        for check_number in winning_numbers:
            if check_number in playing_numbers:
                cleaned_cards[card_id]["match_count"] += 1
        if cleaned_cards[card_id]["match_count"] > 0:
            cleaned_cards[card_id]["points_earned"] = 2**(cleaned_cards[card_id]["match_count"]-1)
        else:
            pass
    return cleaned_cards


def sum_card_results(counted_cards: dict) -> int:
    points_won = 0
    for card_id, card_details in counted_cards.items():
        points_won += card_details["points_earned"]
    return points_won


def count_with_copies(counted_cards: dict) -> dict:
    # Initialize all cards with a count of 1
    for card_id, card_details in counted_cards.items():
        card_details["copies"] = 1
    for card_id, card_details in counted_cards.items():
        for i in range(0, card_details["copies"]):
            current_card_id = card_details["card_id"]
            count_of_cards_to_increment = card_details["match_count"]
            for j in range(1, count_of_cards_to_increment+1):
                counted_cards[current_card_id + j]["copies"] += 1

    return counted_cards


def sum_copied_cards(copied_card_dict: dict) -> int:
    total_copies = 0
    for card_id, card_details in copied_card_dict.items():
        total_copies += card_details["copies"]
    return total_copies


if __name__ == '__main__':
    input_file = 'official_input.txt'
    parsed_cards = parse_input_file(input_file)

    my_counted_cards = count_card_results(parsed_cards)
    for k, v in my_counted_cards.items():
        print(f"{k}, {v}")
    print()

    print(f"These cards are worth this many points: {sum_card_results(my_counted_cards)}\n")
    # Correct value - 27059 :) got this!

    my_cards_with_copies = count_with_copies(my_counted_cards)
    for k, v in my_counted_cards.items():
        print(f"{k}, {v}")
    print()

    copied_card_sum = sum_copied_cards(my_cards_with_copies)
    print(f"There are this many total scratchcards under the new pattern: {copied_card_sum}")
    # Correct value - 5744979 :) got this!
