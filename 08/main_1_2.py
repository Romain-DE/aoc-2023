from __future__ import annotations


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


def create_element_list(elements_as_str: str) -> list[tuple]:
    return [
        (
            eq_elt.split(" = ")[0],
            (
                eq_elt.split(" = ")[1].replace("(", "").replace(")", "").split(", ")[0],
                eq_elt.split(" = ")[1].replace("(", "").replace(")", "").split(", ")[1],
            ),
        )
        for eq_elt in elements_as_str.split("\n")
    ]


elements = elements = Parser().elements
elements_list = create_element_list(elements)


class Node:
    def __init__(self, value):
        self.value: str = value
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None
        self.visited_nodes = set()

    def insert(self, parent, children):
        if self.root is None:
            self.root = Node(parent)
            self.root.left = Node(children[0])
            self.root.right = Node(children[1])
        else:
            self._insert(parent, children, self.root)

    def _insert(self, parent, children, current_node):
        if current_node.value == parent:
            current_node.left = Node(children[0])
            current_node.right = Node(children[1])
        else:
            if current_node.left is not None:
                self._insert(parent, children, current_node.left)
            if current_node.right is not None:
                self._insert(parent, children, current_node.right)

    def afficher(self):
        self.visited_nodes = set()
        self._afficher(self.root, 0)

    def _afficher(self, noeud, niveau, position=None):
        if noeud:
            if noeud.value in self.visited_nodes:
                print("  " * niveau + f"{noeud.value} (circularité détectée)")
                return

            self.visited_nodes.add(noeud.value)

            caractere_branche = self._obtenir_caractere_branche(position)

            self._afficher(noeud.right, niveau + 1, position="right")
            print("  " * niveau + caractere_branche + str(noeud.value))
            self._afficher(noeud.left, niveau + 1, position="left")

    def _obtenir_caractere_branche(self, position):
        if position == "left":
            return "└── "
        elif position == "right":
            return "├── "
        else:
            return ""

    def get_or_create_node_child(
        self, current_node: Node, child_node: Node, left=True
    ) -> Node:
        if child_node:
            return child_node
        else:
            full_current_node_as_tuple = [
                elt for elt in elements_list if elt[0] == current_node.value
            ][0]  # toujours bof ça. Stocker dans un dict plutôt ?
            position = 0 if left else 1
            self.insert(
                parent=full_current_node_as_tuple[0],
                children=full_current_node_as_tuple[1],
            )
            return Node(full_current_node_as_tuple[1][position])

    def apply_instruction(self, instruction: str, current_node: Node) -> Node:
        if instruction == "L":
            return self.get_or_create_node_child(
                current_node, current_node.left, left=True
            )
        elif instruction == "R":
            return self.get_or_create_node_child(
                current_node, current_node.right, left=False
            )
        else:
            print("wrong instruction")
            raise NameError

    def apply_list_of_instructions(
        self, instructions: list[str], starting_node: Node = None
    ) -> Node:
        if starting_node == None:
            starting_node = self.root
        for i in instructions:
            starting_node = self.apply_instruction(i, starting_node)
        return starting_node

    def apply_list_of_instructions_it(
        self, instructions: list[str], iterations: int, starting_node: Node = None
    ) -> Node:
        if starting_node == None:
            starting_node = self.root
        for _ in range(iterations):
            for i in instructions:
                starting_node = self.apply_instruction(i, starting_node)
        return starting_node


def is_destination_reached(current_node: Node, dest_name: str) -> bool:
    return current_node.value == dest_name


def is_wildcard_destination_reached(current_node: Node, wildcard_ending: str) -> bool:
    return current_node.value.endswith(wildcard_ending)


instructions = Parser().instructions

arbre = BinaryTree()
arbre.insert("AAA", ("FPG", "LTD"))

destination = False
j = 1

while not destination:
    print("## step", j, "##")
    noeud_arrivée = arbre.apply_list_of_instructions_it(instructions, j)
    destination = is_destination_reached(noeud_arrivée, "ZZZ")
    print(destination)
    j += 1
    if j > 50:
        break

# true at iteration #43


### PART 2
starting_node_names = ["RMA", "NXA", "GDA", "PLA", "QLA", "AAA"]
list_of_node_tuples = [
    node_tuple for node_tuple in elements_list if node_tuple[0] in starting_node_names
]
print(list_of_node_tuples)


for i, tuple in enumerate(list_of_node_tuples):
    print("### ROUND", i, "###")
    print(tuple[0])
    j = 50
    destination = False
    arbre = BinaryTree()
    arbre.insert(parent=tuple[0], children=tuple[1])
    while not destination:
        print("## step", j, "##")
        noeud_arrivée = arbre.apply_list_of_instructions_it(instructions, j)
        destination = is_wildcard_destination_reached(noeud_arrivée, "Z")
        if destination:
            print(destination)
        j += 1
        if j > 100:
            break

# RMA : 79
# NXA : 71
# GDA : 53
# PLA : 61
# QLA : 47
# AAA : 43

print(36648605837 * len(instructions))
