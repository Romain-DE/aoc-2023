from __future__ import annotations
from typing import Optional


class Parser(object):
    def __init__(self) -> None:
        self.data = self._read()
        self.instructions = list(self.get_instructions(self.data))
        self.elements = self.get_elements(self.data)

    def _read(self) -> str:
        with open("08/input.txt", "r") as file:
            data = file.read()
        return data

    def get_instructions(self, raw_data) -> list[str]:
        return list(raw_data.split("\n\n")[0])

    def get_elements(self, raw_data) -> str:
        return raw_data.split("\n\n")[1]


# Idéalement : pouvoir implémenterun élément juste avec le nom
class Element(object):
    def __init__(self, name, left_name=None, right_name=None) -> None:
        self.name: str = name
        # self.left: Element = left if left else self._get_left()
        # self.right: Element = right if right else self._get_right()
        self.left_name: str = left_name  # self._get_left().name # Bizarre ou pas ?
        self.right_name: str = right_name  # self._get_right().name

    # def _get_left(self) -> Element:
    #     return [elt for elt in elements_list if elt.name == self.left_name][0]

    # def _get_right(self) -> Element:
    #     return [elt for elt in elements_list if elt.name == self.right_name][0]

    # See if useful
    def __eq__(self, other: Element) -> bool:
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return self.name

    def apply_instruction(self, instruction: str) -> Element:
        if instruction == "L":
            return self._get_left()  # pas terrible
        elif instruction == "R":
            return self._get_right()
        else:
            print("wrong instruction")
            raise NameError

    def apply_list_of_instructions(self, instructions: list[str]) -> Element:
        for i in instructions:
            self = self.apply_instruction(i)
        return self

    def apply_list_of_instructions_it(
        self, instructions: list[str], iterations: int
    ) -> Element:
        for j in range(iterations):
            for i in instructions:
                self = self.apply_instruction(i)
        return self

    def is_destination_reached(self, dest_name: str) -> bool:
        return self.name == dest_name

    def is_wildcard_destination_reached(self, wildcard_ending: str) -> bool:
        return self.name.endswith(wildcard_ending)


# 0. Comment stocker la donnée ? un dict ? une liste d'éléments ?
# 1. Ecrire une fonction qui prend en argument une instruction (L/R) et un élément (AAA, etc.), et qui renvoie l'élément
# 2. Voir comment chaîner les fonctions et tester sur l'exemple RL. La fonction qui chaîne les fonctions doit garder un compte


instructions = Parser().instructions


def create_element_list(elements_as_str: str) -> list[Element]:
    return [
        Element(
            eq_elt.split(" = ")[0],
            Element(
                eq_elt.split(" = ")[1].replace("(", "").replace(")", "").split(", ")[0]
            ),
            Element(
                eq_elt.split(" = ")[1].replace("(", "").replace(")", "").split(", ")[1]
            ),
        )
        for eq_elt in elements_as_str.split("\n")
    ]


elements = Parser().elements
elements_list = create_element_list(elements)
print(instructions)

# PART 1

# for i in range(45):
#     print("## step", i, "##")
#     print(Element("AAA", "FPG", "LTD").apply_list_of_instructions_it(instructions, i).is_destination_reached("ZZZ"))

# true at iteration #43
print(44 * len(instructions))  # too high : 12188
print(43 * len(instructions))  # good : 11911


### PART 2
class Nodes(object):
    def __init__(self, *elements) -> None:
        self.elements: list[Element] = elements

    def __repr__(self) -> str:
        return ", ".join([elt.name for elt in self.elements])

    def is_wildcard_destination_reached_for_everyone(
        self, wildcard_ending: str
    ) -> bool:
        return all(
            [
                elt.is_wildcard_destination_reached(wildcard_ending)
                for elt in self.elements
            ]
        )

    def apply_list_of_instructions_it(
        self, instructions: list[str], iterations: int
    ) -> Nodes:
        return Nodes(
            *[
                elt.apply_list_of_instructions_it(instructions, iterations)
                for elt in self.elements
            ]
        )


# print(Element("AAA").apply_list_of_instructions_it(["L", "L", "R"], 2).is_destination_reached(Element("ZZZ")))
# elements_list = Element("AAA").create_element_list(Parser().elements)

# elements_as_str = [("RMA"), "NXA", "GDA", "PLA", "QLA", "AAA"]
# nodes = Nodes(*[elt for elt in elements_list if elt.name in elements_as_str])
# print(nodes)

# for i in range(10):
#     print("## step", i, "##")
#     print(nodes.apply_list_of_instructions_it(instructions, i).is_wildcard_destination_reached_for_everyone("Z"))
# rien jusqu'au step 199
