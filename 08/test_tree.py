from collections import deque
from main_with_trees import Parser


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


class Noeud:
    def __init__(self, valeur):
        self.valeur = valeur
        self.gauche = None
        self.droite = None


class ArbreBinaire:
    def __init__(self):
        self.racine = None
        self.noeuds_visites = set()

    def inserer(self, parent, enfants):
        if self.racine is None:
            self.racine = Noeud(parent)
            self.racine.gauche = Noeud(enfants[0])
            self.racine.droite = Noeud(enfants[1])
        else:
            self._inserer(parent, enfants, self.racine)

    def _inserer(self, parent, enfants, noeud_actuel):
        if noeud_actuel.valeur == parent:
            noeud_actuel.gauche = Noeud(enfants[0])
            noeud_actuel.droite = Noeud(enfants[1])
        else:
            if noeud_actuel.gauche is not None:
                self._inserer(parent, enfants, noeud_actuel.gauche)
            if noeud_actuel.droite is not None:
                self._inserer(parent, enfants, noeud_actuel.droite)

    def afficher(self):
        self.noeuds_visites = set()
        self._afficher(self.racine, 0)

    def _afficher(self, noeud, niveau, position=None):
        if noeud:
            if noeud.valeur in self.noeuds_visites:
                print("     " * niveau + f"{noeud.valeur} (circularité détectée)")
                return

            self.noeuds_visites.add(noeud.valeur)

            caractere_branche = self._obtenir_caractere_branche(position)

            self._afficher(noeud.droite, niveau + 1, position="droite")
            print("     " * niveau + caractere_branche + str(noeud.valeur))
            self._afficher(noeud.gauche, niveau + 1, position="gauche")

    def _obtenir_caractere_branche(self, position):
        if position == "gauche":
            return "└── "
        elif position == "droite":
            return "├── "
        else:
            return ""

    def parcours_largeur(self):
        if self.racine is None:
            return []

        resultat = []
        file_attente = deque([self.racine])

        while file_attente:
            noeud_actuel = file_attente.popleft()
            resultat.append(noeud_actuel.valeur)

            if noeud_actuel.gauche:
                file_attente.append(noeud_actuel.gauche)
            if noeud_actuel.droite:
                file_attente.append(noeud_actuel.droite)

        return resultat

    def get_or_create_node_child(self, current_node: Noeud, child_node: Noeud) -> Noeud:
        if child_node:
            return child_node
        else:
            full_current_node_as_tuple = [
                elt for elt in elements_list if elt[0] == current_node.valeur
            ][0]
            self.inserer(
                full_current_node_as_tuple[0], full_current_node_as_tuple[1]
            )  # insérer ici le noeuf actuelle
            return Noeud(full_current_node_as_tuple[1][0])

    def apply_instruction(self, instruction: str, current_node: Noeud) -> Noeud:
        if instruction == "L":
            return self.get_or_create_node_child(current_node, current_node.gauche)
        elif instruction == "R":
            return self.get_or_create_node_child(current_node, current_node.droite)
        else:
            print("wrong instruction")
            raise NameError

    def apply_list_of_instructions(
        self, instructions: list[str], starting_node: Noeud = None
    ) -> Noeud:
        if starting_node == None:
            starting_node = self.racine
        for i in instructions:
            starting_node = self.apply_instruction(i, starting_node)
        return starting_node

    def apply_list_of_instructions_it(
        self, instructions: list[str], iterations: int, starting_node: Noeud = None
    ) -> Noeud:
        if starting_node == None:
            starting_node = self.racine
        for _ in range(iterations):
            for i in instructions:
                starting_node = self.apply_instruction(i, starting_node)
        return starting_node

    def is_destination_reached(self, current_node: Noeud, dest_name: str) -> bool:
        return current_node.valeur == dest_name

    def is_wildcard_destination_reached(
        self, current_node: Noeud, wildcard_ending: str
    ) -> bool:
        return current_node.valeur.endswith(wildcard_ending)


# Exemple d'utilisation avec votre structure
# arbre = ArbreBinaire()
# relations = [("AAA", ("BBB", "CCC")),
#              ("BBB", ("BB1", "BB2")),
#              ("CCC", ("CC1", "CC2")),
#              ("CC1", ("C11", "AAA"))]

# for parent, enfants in relations:
#     arbre.inserer(parent, enfants)

# arbre.afficher()
# print(arbre.parcours_largeur())


instructions = Parser().instructions
arbre_2 = ArbreBinaire()

arbre_2.inserer("AAA", ("FPG", "LTD"))
# for parent, enfants in elements_list:
#     arbre_2.inserer(parent, enfants)
# noeud_arrivée = arbre_2.apply_list_of_instructions_it(instructions, 45)
# print(arbre_2.is_destination_reached(noeud_arrivée, "ZZZ"))
# arbre_2.afficher()


for i in range(56):
    print("## step", i, "##")
    noeud_arrivée = arbre_2.apply_list_of_instructions_it(instructions, i)
    print(arbre_2.is_destination_reached(noeud_arrivée, "ZZZ"))

# true at iteration #43

# ça amrche pas. Tester avec l'exemple pour voir ce qui déconne
