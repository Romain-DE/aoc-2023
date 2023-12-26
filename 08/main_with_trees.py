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


# Nouvelle idée : implémenter une structure d'arbre
class Node(object):
    def __init__(self, name, left=None, right=None) -> None:
        self.name: str = name
        self.left: Optional[Node] = left
        self.right: Optional[Node] = right

    def __repr__(self) -> str:
        if (self.left is not None) & (self.right is not None):
            return "(" + self.name + ", " + self.left + ", " + self.right + ")"
        else:
            return self.name

    def __eq__(self, other: Node) -> bool:
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


class Tree(object):
    def __init__(self) -> None:
        self.root: Node = None

    def add(self, val):
        if not self.root:
            self.root = Node(val)
        else:
            self._add(val, self.root)

    def _add(self, val, node):
        if val < node.v:
            if node.l:
                self._add(val, node.l)
            else:
                node.l = Node(val)
        else:
            if node.r:
                self._add(val, node.r)
            else:
                node.r = Node(val)

    def _bfs_find(self, node: Node) -> Optional[Node]:
        if self.root == None:
            print("Empty tree")
            raise KeyError
        else:
            pass

    def iterate_through_tree(
        self, starting_node: Node = None, list_of_nodes: list[Node] = []
    ) -> list[Node]:
        if starting_node == None:
            starting_node == self.root
        # Adding L and R nodes
        if left := starting_node.left:
            if left not in list_of_nodes:
                list_of_nodes.append(left)
            else:
                if left.hasChild():  # TODO
                    return list_of_nodes  # et on attend pas la droite ? Si, faire la vérif des deux cots
        if right := starting_node.right:
            if right not in list_of_nodes:
                list_of_nodes.append(right)

        if starting_node.left is not None:
            self.iterate_through_tree(starting_node.left, list_of_nodes)
        if starting_node.right is not None:
            self.iterate_through_tree(starting_node.right, list_of_nodes)

        return list_of_nodes

    # Deux fonctions find
    # une avec toutes les précautions nécessaires:  est-ce que la clé existe, etc.
    # une


print(Node("AAA", "BBB", "CCC"))
# a = Tree("AAA").add_children("BBB", "CCC")
# print(a.left)

# t =  Tree(
#         Node(
#             "AAA",
#             Node("BBB", Node("BB1", Node("B11"), Node("B22")), Node("BB2")),
#             Node("CCC", Node("CC1"), Node("C2")),
#         )
#     )
# print(t.iterate_through_tree())
# print(Tree("AAA"))
# Idées pour le BTree
# 1. Créer une liste avec tous les noeuds
# 2. Créer une fonction "ajouter un noeud". Comment faire? Specifier l'endroit où on l'ajoute ?
# https://stackoverflow.com/questions/2598437/how-to-implement-a-binary-tree
# 3. Créer une fonciton "ce noeud est dans le tree ?"
# 4. Créer une fonction qui parcourt le tree à partir d'instructions et qui ajoute un noeud si besoin
# Bonus : voir si existe repr sympa


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


elements = Parser().elements
elements_list = create_element_list(elements)
# print(elements_list)
