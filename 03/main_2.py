import re
from typing import Any, Dict
from functools import reduce

with open("03/input.txt", "r") as file:
    data = file.read()
    data_by_line = data.split("\n")


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


def create_list_of_sign_dicts_from_line_number(
    line_number: int,
) -> list[Dict[str, int]]:
    line = data_by_line[line_number]
    line_matches = re.finditer(r"\*", line)
    list_of_star_dicts = []

    for elt in line_matches:
        list_of_star_dicts.append({"x_pos": elt.start(), "numbers_around": []})

    return list_of_star_dicts


def return_list_of_signs_on_same_line(
    x_start_pos: int, length: int, line_number: int
) -> list[tuple((int, int))]:
    list_of_star_dicts = create_list_of_sign_dicts_from_line_number(line_number)
    list_of_star_x_pos = [star["x_pos"] for star in list_of_star_dicts]
    place_before_nb = x_start_pos - 1
    place_after_nb = x_start_pos + length
    if x_start_pos == 0:
        if place_after_nb in list_of_star_x_pos:
            return [(place_after_nb, line_number)]
        else:
            return []
    elif x_start_pos == 139:
        if place_before_nb in list_of_star_x_pos:
            return [(place_before_nb, line_number)]
        else:
            return []
    else:
        if (place_before_nb in list_of_star_x_pos) & (
            place_after_nb in list_of_star_x_pos
        ):
            return [(place_before_nb, line_number), (place_after_nb, line_number)]
        elif place_before_nb in list_of_star_x_pos:
            return [(place_before_nb, line_number)]
        elif place_after_nb in list_of_star_x_pos:
            return [(place_after_nb, line_number)]
        else:
            return []


def return_list_of_signs_on_adjacent_line(
    x_start_pos: int, length: int, line_number: int, below=True
) -> list[tuple((int, int))]:
    if below:
        offset = 1
    else:
        offset = -1
    star_dicts_in_adjacent_line = create_list_of_sign_dicts_from_line_number(
        line_number + offset
    )
    list_of_star_x_pos = [star["x_pos"] for star in star_dicts_in_adjacent_line]

    place_before = x_start_pos - 1
    place_after = x_start_pos + length
    if x_start_pos == 0:
        list_of_possible_x_pos = list(range(x_start_pos, place_after + 1))
    elif x_start_pos == 139:
        list_of_possible_x_pos = list(range(place_before, x_start_pos))
    else:
        list_of_possible_x_pos = list(range(place_before, place_after + 1))

    return [
        (x_pos, line_number + offset)
        for x_pos in list_of_possible_x_pos
        if x_pos in list_of_star_x_pos
    ]


def return_list_of_signs_from_below_or_above(
    x_start_pos: int, length: int, line_number: int
) -> list[tuple((int, int))]:
    if line_number == 0:
        return return_list_of_signs_on_adjacent_line(x_start_pos, length, line_number)
    elif line_number == 139:
        return return_list_of_signs_on_adjacent_line(
            x_start_pos, length, line_number, below=False
        )
    else:
        return return_list_of_signs_on_adjacent_line(
            x_start_pos, length, line_number
        ) + return_list_of_signs_on_adjacent_line(
            x_start_pos, length, line_number, below=False
        )


def return_signs_around_number(nb_dict: Dict[str, int]) -> bool:
    star_list = return_list_of_signs_from_below_or_above(
        nb_dict["x_start_pos"], nb_dict["length"], nb_dict["line_number"]
    ) + return_list_of_signs_on_same_line(
        nb_dict["x_start_pos"], nb_dict["length"], nb_dict["line_number"]
    )
    nb_dict["stars_around"] = star_list
    return nb_dict


# Meilleure idée : renverser le point de vue, utiliser la position des * et voir s'il y a des nb autour
# On parcourt chaque étoile, et on regarde les chiffres autour. A chaque fois qu'on en voit un, on ajoute un élément à la liste du champ "numbers_around"
# PB : comment on sait que pour une étoile en position (i, j),
# Qu'est-ce que ça veut dire voir un chiffre autour ?


# print(create_list_of_sign_dicts_from_line_number(1))
print(create_list_of_dicts_from_line(1))
print(
    return_signs_around_number(
        {"x_start_pos": 19, "line_number": 1, "length": 3, "number": "587"}
    )
)


def list_all_part_numbers() -> list[Dict]:
    part_nb_dicts = []
    for line_number in range(140):
        for nb_dict in create_list_of_dicts_from_line(line_number):
            output_dict = return_signs_around_number(nb_dict)
            if output_dict.get("stars_around"):
                part_nb_dicts.append(output_dict)
    return part_nb_dicts


def create_coordinates_dict_from_nb_dict_list(
    list_of_dicts: list[Dict],
) -> Dict[str, Any]:
    dict_of_coordinates = {}
    for nb_dict in list_of_dicts:
        for coord_tuple in nb_dict["stars_around"]:
            if str(coord_tuple) in dict_of_coordinates:
                dict_of_coordinates[str(coord_tuple)].append(int(nb_dict["number"]))
            else:
                dict_of_coordinates[str(coord_tuple)] = [int(nb_dict["number"])]

    return dict_of_coordinates


def filter_dicts_of_coord_with_value_of_len_2(
    dict_of_coordinates: Dict[str, list],
) -> Dict[str, list]:
    return {key: value for key, value in dict_of_coordinates.items() if len(value) == 2}


def create_dict_of_multiplied_values(
    filtered_dict_of_coordinates: Dict,
) -> Dict[str, int]:
    product_dict = {}
    for coord, value_list in filtered_dict_of_coordinates.items():
        product_dict[coord] = reduce(lambda x, y: x * y, value_list)
    return product_dict


def sum_values_in_product_dict(product_dict: Dict[str, int]) -> int:
    sum = 0
    for _, value in product_dict.items():
        sum = sum + value

    return sum


list_of_part_nb = list_all_part_numbers()
dict_of_coords = create_coordinates_dict_from_nb_dict_list(list_of_part_nb)
filtered_dict_of_coord = filter_dicts_of_coord_with_value_of_len_2(dict_of_coords)
product_dict = create_dict_of_multiplied_values(filtered_dict_of_coord)
sum_of_gear = sum_values_in_product_dict(product_dict)

print(sum_of_gear)

### TEST PART ###
print(list_all_part_numbers()[:11])

sample_list = [
    {
        "x_start_pos": 25,
        "line_number": 0,
        "length": 1,
        "number": "3",
        "stars_around": [(24, 1)],
    },
    {
        "x_start_pos": 65,
        "line_number": 0,
        "length": 2,
        "number": "94",
        "stars_around": [(64, 1)],
    },
    {
        "x_start_pos": 82,
        "line_number": 0,
        "length": 3,
        "number": "806",
        "stars_around": [(82, 1)],
    },
    {
        "x_start_pos": 131,
        "line_number": 0,
        "length": 3,
        "number": "186",
        "stars_around": [(133, 1)],
    },
    {
        "x_start_pos": 15,
        "line_number": 1,
        "length": 3,
        "number": "574",
        "stars_around": [(14, 1)],
    },
    {
        "x_start_pos": 19,
        "line_number": 1,
        "length": 3,
        "number": "587",
        "stars_around": [(19, 2)],
    },
    {
        "x_start_pos": 33,
        "line_number": 1,
        "length": 3,
        "number": "161",
        "stars_around": [(36, 2)],
    },
    {
        "x_start_pos": 52,
        "line_number": 1,
        "length": 3,
        "number": "412",
        "stars_around": [(51, 2)],
    },
    {
        "x_start_pos": 122,
        "line_number": 1,
        "length": 3,
        "number": "637",
        "stars_around": [(121, 2)],
    },
    {
        "x_start_pos": 7,
        "line_number": 2,
        "length": 3,
        "number": "831",
        "stars_around": [(9, 3)],
    },
    {
        "x_start_pos": 12,
        "line_number": 2,
        "length": 2,
        "number": "33",
        "stars_around": [(14, 1)],
    },
]

sample_dict_of_coord = create_coordinates_dict_from_nb_dict_list(sample_list)

filtered_dict = {
    key: value for key, value in sample_dict_of_coord.items() if len(value) == 2
}

print(filtered_dict_of_coord)
