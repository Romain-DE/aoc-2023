from typing import Any, Dict
from main_1 import create_list_from_card, format_lists, intersect_lists
import copy

with open("04/input.txt", "r") as file:
    data = file.read().split("\n")


def calculate_card_score(intersection: set[int]) -> int:
    matches = len(intersection)
    return matches


functions = [create_list_from_card, format_lists, intersect_lists, calculate_card_score]


def method_chaining(game_line: str) -> bool:
    output = game_line
    for func in functions:
        output = func(output)
    return output


def create_initial_dict() -> Dict[str, Any]:
    dict_of_cards = {}
    for index, data_line in enumerate(data):
        points = method_chaining(
            data_line
        )  # Attention : ici il faut oublier le coup des puissances
        card_number = index + 1
        dict_of_cards[card_number] = {}
        dict_of_cards[card_number]["points"] = points
        dict_of_cards[card_number]["card_added"] = [
            x for x in range(card_number + 1, card_number + 1 + points) if x <= 192
        ]
        dict_of_cards[card_number]["number_of_instances"] = 1

    return dict_of_cards


initial_dict = create_initial_dict()


def increment_nb_of_instances(initial_dict: Dict[str, Any]) -> Dict[str, Any]:
    copy_dict = copy.deepcopy(initial_dict)
    for card_number, card_values in copy_dict.items():
        for number in card_values["card_added"]:
            copy_dict[number]["number_of_instances"] += card_values[
                "number_of_instances"
            ]

    return copy_dict


def compute_sum_of_instances(incremented_dict: Dict[str, Any]) -> int:
    total_nb_of_instances = 0
    for card_values in incremented_dict.values():
        total_nb_of_instances += card_values["number_of_instances"]

    return total_nb_of_instances


initial_dict = create_initial_dict()
incremented_dict = increment_nb_of_instances(initial_dict)
total_nb_of_instances = compute_sum_of_instances(incremented_dict)


print(incremented_dict)
print(total_nb_of_instances)  # 5483 too low, 980 too low

# il manque les multiplications par le nb de cartes !
