import re
from typing import Dict

with open("03/input.txt", "r") as file:
    data = file.read()
    data_by_line = data.split("\n")

special_signs = list(set(re.sub("\d|\.", "", data)))


def create_list_of_dicts_from_line(line_number: int) -> list[Dict]:
    line = data_by_line[line_number]
    line_matches = re.finditer(r"\d+", line)
    list_of_dicts = []
    for elt in line_matches:
        list_of_dicts.append(
            {
                "x_start_pos": elt.start(),
                "line_number": line_number,
                "length": elt.end() - elt.start(),
                "number": elt.group(),
            }
        )

    return list_of_dicts


def create_list_of_signs_from_line_number(line_number: int) -> list[int]:
    line = data_by_line[line_number]
    line_matches = re.finditer(r"\%|\/|\=|\+|\-|\#|\$|\&|\@|\*", line)
    list_of_x_pos = []
    for elt in line_matches:
        list_of_x_pos.append(elt.start())

    return list_of_x_pos


def check_if_has_sign_next_to_it(
    x_start_pos: int, length: int, line_number: int
) -> bool:
    list_of_signs = create_list_of_signs_from_line_number(line_number)
    if x_start_pos == 0:
        return x_start_pos + length in list_of_signs
    elif x_start_pos == 139:
        return x_start_pos - 1 in list_of_signs
    else:
        return (x_start_pos - 1 in list_of_signs) | (
            x_start_pos + length in list_of_signs
        )


def check_if_has_sign_on_adjacent_line(
    x_start_pos: int, length: int, line_number: int, below=True
) -> bool:
    if below:
        offset = 1
    else:
        offset = -1
    signs_pos_in_line_below = create_list_of_signs_from_line_number(
        line_number + offset
    )
    if x_start_pos == 0:
        list_of_possible_x_pos = list(range(x_start_pos, x_start_pos + length + 1))
    elif x_start_pos == 139:
        list_of_possible_x_pos = list(range(x_start_pos - 1, x_start_pos))
    else:
        list_of_possible_x_pos = list(range(x_start_pos - 1, x_start_pos + length + 1))
    return any([x_pos in signs_pos_in_line_below for x_pos in list_of_possible_x_pos])


def check_if_has_sign_below_or_above(
    x_start_pos: int, length: int, line_number: int
) -> bool:
    if line_number == 0:
        return check_if_has_sign_on_adjacent_line(x_start_pos, length, line_number)
    elif line_number == 139:
        return check_if_has_sign_on_adjacent_line(
            x_start_pos, length, line_number, below=False
        )
    else:
        return check_if_has_sign_on_adjacent_line(
            x_start_pos, length, line_number
        ) | check_if_has_sign_on_adjacent_line(
            x_start_pos, length, line_number, below=False
        )


print(check_if_has_sign_below_or_above(2, 3, 2))


def check_if_is_part_number(nb_dict: Dict[str, int]) -> bool:
    if check_if_has_sign_next_to_it(
        nb_dict["x_start_pos"], nb_dict["length"], nb_dict["line_number"]
    ) | check_if_has_sign_below_or_above(
        nb_dict["x_start_pos"], nb_dict["length"], nb_dict["line_number"]
    ):
        return True
    else:
        return False


check_if_is_part_number(
    {"x_start_pos": 25, "line_number": 0, "length": 1, "number": "3"}
)


def list_all_part_numbers_in_line(line_number: int) -> list[int]:
    part_nb = []
    for nb_dict in create_list_of_dicts_from_line(line_number):
        if check_if_is_part_number(nb_dict):
            part_nb.append(nb_dict["number"])
    return part_nb


def list_all_part_numbers() -> list[int]:
    part_nb = []
    for line_number in range(140):
        for nb_dict in create_list_of_dicts_from_line(line_number):
            if check_if_is_part_number(nb_dict):
                part_nb.append(int(nb_dict["number"]))
    return part_nb


part_nb = list_all_part_numbers()
print(sum(part_nb))
