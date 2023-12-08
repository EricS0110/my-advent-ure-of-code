data_list = []
with open("official_input.txt", "r") as data:
    for line in data:
        game_split_1 = line.split(' ')
        data_list.append((game_split_1[0], int(game_split_1[1])))


def mapper(hand):
    pair, two_pair, three_kind, four_kind, five_kind = False, False, False, False, False

    # First remove jokers, to decide hand without jokers.
    no_jokers = hand.replace("J","")
    for c in "AKQT98765432":
        count = no_jokers.count(c)
        if count == 2:
            pair, two_pair = (False,True) if pair else (True,False)
        if count == 3:
            three_kind = True
        if count == 4:
            four_kind = True
        if count == 5:
            five_kind = True

    # Then add back jokers, enhancing the hand as they are added back
    for j in range(hand.count("J")):
        if four_kind:
            five_kind, four_kind = True, False
        elif three_kind:
            four_kind, three_kind = True, False
        elif two_pair:
            pair, two_pair, three_kind = True, False, True
        elif pair:
            pair, three_kind = False, True
        else:
            pair = True

    # Prefix the item, with a letter indicating type of hand, which is sorted first.
    if five_kind:
        key = "Z" + hand
    elif four_kind:
        key = "Y" + hand
    elif three_kind and pair:
        key = "X" + hand
    elif three_kind:
        key = "W" + hand
    elif two_pair:
        key = "V" + hand
    elif pair:
        key = "U" + hand
    else:
        key = "T" + hand

    # replace chars AKQJT, with FED1B, to ensure rest of hand is sorted correctly
    key = key.replace("A", "F") \
        .replace("K", "E") \
        .replace("Q", "D") \
        .replace("J", "1") \
        .replace("T", "B")

    return key


data_list.sort(key=lambda itm: mapper(itm[0]))

i = 0
total = 0
for item in data_list:
    i += 1
    total += item[1] * i

print(total)
