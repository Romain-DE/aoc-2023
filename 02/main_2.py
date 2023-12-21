from typing import Dict
import re


with open("02/input.txt", "r") as file:
    data = file.read().split("\n")


def get_colours_in_game(game_line: str) -> list[str]:
    list_of_colours = game_line.split(":")[1].replace(";", ",").split(",")
    return list_of_colours


print(
    get_colours_in_game(
        "Game 20: 1 blue, 9 green, 2 red; 2 blue, 4 red, 4 green; 4 green, 2 red"
    )
)
colours = ["red", "green", "blue"]


def create_dict_from_game(game_list: list[str]) -> Dict[str, int]:
    colour_dict = {colour: [] for colour in colours}
    for colour in colours:
        for elt in game_list:
            if colour in elt:
                colour_dict[colour].append(int(re.sub("\D", "", elt)))
        colour_dict[colour] = max(colour_dict[colour])

    return colour_dict


def compute_power_of_game(game: Dict[str, int]) -> int:
    i = 1
    for j in list(game.values()):
        i = i * j
    return i


print(
    create_dict_from_game(
        [
            " 1 blue",
            " 9 green",
            " 2 red",
            " 2 blue",
            " 4 red",
            " 4 green",
            " 4 green",
            " 2 red",
        ]
    )
)

print(compute_power_of_game({"red": 4, "green": 9, "blue": 2}))

functions = [get_colours_in_game, create_dict_from_game, compute_power_of_game]


def method_chaining(game_line: str) -> bool:
    output = game_line
    for func in functions:
        output = func(output)
    return output


power_list = [method_chaining(game_line) for game_line in data]

print(power_list)
print(sum(power_list))
