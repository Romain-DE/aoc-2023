from typing import Dict
import re


with open("02/input.txt", "r") as file:
    data = file.read().split("\n")


def create_sets_from_game(game_line: str) -> list[str]:
    list_of_sets = game_line.split(":")[1].split(";")
    return list_of_sets


print(create_sets_from_game(data[0]))


def create_unit_dict_from_set_result(input_set: str) -> Dict[str, int]:
    cube_list = input_set.split(",")
    set_dict = {"red": 0, "green": 0, "blue": 0}
    for cube_type in cube_list:
        for colour in ["red", "green", "blue"]:
            if colour in cube_type:
                set_dict[colour] = int(re.sub("\D", "", cube_type))
    return set_dict


print(create_unit_dict_from_set_result("12 green, 4 red, 2 blue"))


def create_dicts_from_sets(input_sets: list[str]) -> list[Dict[str, int]]:
    return [create_unit_dict_from_set_result(input_set) for input_set in input_sets]


print(
    create_dicts_from_sets(
        "10 red, 7 green, 3 blue; 5 blue, 3 red, 10 green; 4 blue, 14 green, 7 red; 1 red, 11 green; 6 blue, 17 green, 15 red; 18 green, 7 red, 5 blue".split(
            ";"
        )
    )
)


def is_set_valid(input_dict: Dict[str, int]) -> bool:
    R_CUBES = 12
    G_CUBES = 13
    B_CUBES = 14
    conditions = [
        input_dict["red"] <= R_CUBES,
        input_dict["green"] <= G_CUBES,
        input_dict["blue"] <= B_CUBES,
    ]
    return all(conditions)


def is_game_valid(list_of_sets: list[Dict[str, int]]) -> bool:
    return all([is_set_valid(input_set) for input_set in list_of_sets])


functions = [create_sets_from_game, create_dicts_from_sets, is_game_valid]


def validity_check(game_line: str) -> bool:
    output = game_line
    for func in functions:
        output = func(output)
    return output


bool_list = [validity_check(game_line) for game_line in data]
print(bool_list)
print(len(bool_list))
print(sum([i + 1 for i, game_result in enumerate(bool_list) if game_result]))
