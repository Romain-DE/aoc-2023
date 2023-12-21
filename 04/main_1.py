from typing import Dict
import re
from functools import reduce


with open("04/input.txt", "r") as file:
    data = file.read().split("\n")


def create_list_from_card(card_number: str) -> list[str]:
    list_of_nb = card_number.split(":")[1].split("|")
    return list_of_nb


def format_lists(list_of_nb: list[str]) -> list[set[int]]:
    return [
        set([int(elt) for elt in nb_list.strip().split(" ") if elt != ""])
        for nb_list in list_of_nb
    ]


def intersect_lists(formatted_lists: list[set[int]]) -> set[int]:
    return reduce(lambda x, y: x.intersection(y), formatted_lists)


def calculate_card_score(intersection: set[int]) -> int:
    matches = len(intersection)
    if matches == 0:
        return 0
    else:
        return 2 ** (matches - 1)


functions = [create_list_from_card, format_lists, intersect_lists, calculate_card_score]


def method_chaining(game_line: str) -> bool:
    output = game_line
    for func in functions:
        output = func(output)
    return output


sum_of_cards = 0
for data_line in data:
    sum_of_cards += method_chaining(data_line)

print(sum_of_cards)


### TEST PART ###


print(
    format_lists(
        [
            " 41 49 12 46 39  9 72 78 24 76 ",
            "  3 28 60 82  2 26 67 75 37 72 64 46 54 13 85 20 10  9 18 99 58  4 57 80 25",
        ]
    )
)

# print('  3 28 60 82  2 26 67 75 37 72 64 46 54 13 85 20 10  9 18 99 58  4 57 80 25'.strip().split(" "))

print(
    intersect_lists(
        [
            {39, 72, 41, 9, 12, 76, 46, 78, 49, 24},
            {
                2,
                3,
                4,
                9,
                10,
                13,
                18,
                20,
                25,
                26,
                28,
                37,
                46,
                54,
                57,
                58,
                60,
                64,
                67,
                72,
                75,
                80,
                82,
                85,
                99,
            },
        ]
    )
)

print(calculate_card_score({72, 9, 46}))
