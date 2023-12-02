import math

VALID_DIGIT_WORDS = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9
    }


def get_simple_digits_from_file(file_path: str) -> list[int]:
    results = [0]  # just a dummy default value
    with open(file_path) as calibration_file:
        for line in calibration_file.readlines():
            digits = []
            for character in line:
                if character.isnumeric():
                    digits.append(character)
            if len(digits) == 0:
                results.append(0)
            elif len(digits) == 1:
                results.append(int(str(digits[0]) + str(digits[0])))
            else:
                two_digits = int(str(digits[0]) + str(digits[-1]))
                results.append(two_digits)
    return results


def does_it_contain_a_digit(current_string: str) -> int | bool:
    for check_digit_word in VALID_DIGIT_WORDS.keys():
        if current_string.__contains__(check_digit_word):
            return VALID_DIGIT_WORDS[check_digit_word]
    return False


def get_complex_digits_from_file(file_path: str) -> list[int]:
    results = [0]  # just a dummy default value

    with open(file_path) as calibration_file:
        for line in calibration_file.readlines():
            # Extract first and last "digit" from the string
            digits = []
            line_save = line.strip()
            line_index = 0
            string_check = ''

            # Need to accommodate the case where two spelled-out numbers share first or last letters
            while line_index < len(line_save):
                if line_save[line_index].isnumeric():  # If the character in question is numeric, record it to digits
                    digits.append(int(line_save[line_index]))
                    line_index += 1
                    string_check = ''
                else:
                    string_check += line_save[line_index]
                    x = does_it_contain_a_digit(string_check)
                    if x:
                        digits.append(int(x))
                        string_check = ''
                    else:
                        line_index += 1

            if len(digits) == 0:
                results.append(0)
                print(0)
            elif len(digits) == 1:
                results.append(int(str(digits[0]) + str(digits[0])))
                print(int(str(digits[0]) + str(digits[0])))
            else:
                two_digits = int(str(digits[0]) + str(digits[-1]))
                results.append(two_digits)
                print(two_digits)


            # This method ALMOST works, unless two spelled-out numbers are sharing first or last letters
            # for character in line:
            #     if character.isdigit():
            #         # If it's a digit, save it and move to the next part
            #         digits.append(int(character))
            #         string_check = ''
            #         line_index += 1
            #     elif character.isalpha():
            #         # Build the word for the digit
            #         string_check += character
            #         # Check if the word forms a valid number name
            #         if string_check in VALID_DIGIT_WORDS:
            #             digits.append(VALID_DIGIT_WORDS[string_check])
            #             string_check = ''
            #             line_index += 1
            #         else:
            #             x = does_it_contain_a_digit(string_check)
            #             if x:
            #                 digits.append(int(x))
            #                 string_check = ''
            #         line_index += 1
            #
            # if len(digits) == 0:
            #     results.append(0)
            #     print(0)
            # elif len(digits) == 1:
            #     results.append(int(str(digits[0]) + str(digits[0])))
            #     print(int(str(digits[0]) + str(digits[0])))
            # else:
            #     two_digits = int(str(digits[0]) + str(digits[-1]))
            #     results.append(two_digits)
            #     print(two_digits)
    return results


if __name__ == '__main__':
    # input_file = 'test_001.txt'
    # input_file = 'test_002.txt'
    # input_file = 'debugger.txt'
    input_file = 'aoc_official_input_file.txt'
    # simple_calibration_values = get_simple_digits_from_file(input_file)
    # print(f"Calibration values: {simple_calibration_values}")
    # print(f"Sum of values from the calibration list: {int(math.fsum(simple_calibration_values))}")
    complex_calibration_values = get_complex_digits_from_file(input_file)
    print(f"Calibration values: {complex_calibration_values}")
    print(f"Sum of values from the calibration list: {int(math.fsum(complex_calibration_values))}")
