import re

with open("input.txt", "r") as file:
    data_list = file.read().split("\n")

accepted_digits = "one, two, three, four, five, six, seven, eight, nine".split(", ")
digits_dict = {letter: str(i + 1) for i, letter in enumerate(accepted_digits)}
reg_str = r"(?=(one|two|three|four|five|six|seven|eight|nine|[1-9]))"

capture_list = [re.findall(reg_str, i) for i in data_list]


def create_sign_list(crypted_input: str) -> list[str]:
    return re.findall(reg_str, crypted_input)


def replace_letters_or_leave_str_digit(list_of_str_int: list[str]) -> list[str]:
    return [digits_dict[x] if len(x) > 1 else x for x in list_of_str_int]


def concat_first_and_last(list_of_int_str: list[str]) -> str:
    return list_of_int_str[0] + list_of_int_str[-1]


def clean_str(input: str) -> int:
    functions = [
        create_sign_list,
        replace_letters_or_leave_str_digit,
        concat_first_and_last,
        int,
    ]
    output = input
    for func in functions:
        output = func(output)

    return output


int_list = [clean_str(x) for x in data_list if x != ""]

print(digits_dict)
print(int_list[:20])
print(sum(int_list))

data_test = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
1fourninesix6sixmjngkmsntrnvmtwonehrn
7pqrstsixteen
""".split("\n")

print(([clean_str(x) for x in data_test if x != ""]))
