import re


class Parser:
    def __init__(self, day, filename="input.txt") -> None:
        self.data = self._read(day, filename)
        self.f_data = self.format_data()
        self.f_data_2 = self.format_data_part_2()

    def _read(self, day, filename) -> str:
        with open(day + "/" + filename, "r") as file:
            data = file.read()
        return data

    def format_data(self) -> list[tuple]:
        list_of_str = self.data.split("\n")
        list_of_tuples = [
            (elt.split(" ")[0], [int(char) for char in elt.split(" ")[1].split(",")])
            for elt in list_of_str
        ]
        return list_of_tuples

    def format_data_part_2(self) -> list[tuple]:
        return [
            ("?".join([line[0] for i in range(5)]), line[1] * 5) for line in self.f_data
        ]


f_data = Parser(day="12", filename="input_test.txt").f_data
f_data_2 = Parser(day="12", filename="input_test.txt").f_data_2


# Notes
# Plusieurs approches possibles : générer toutes les lignes et les filtrer, ou bien générer directement les bonnes
# Etapes
# 1. Créer une fonction qui prend en arg une ligne *complète* et un arrangement, et qui renvoie sa validité
# 3. Créer une fonction qui génère toutes les possibilités de remplissage d'une ligne, indépendamment des regles
# 4. Synthèse : générer toutes les possibilités, ne garder que celles qui obeissent aux regles et les renvoyer

# Détail : idée
# 1. créer une fonction qui cible un groupe et qui crée un dict {"group" : "???", "value" : 2, "before" : ".", "after" : "$" }
# 1.    renvoyer les différentes possibilités de 2 parmi 3
#
# OK mais comment gérer les cas comme ça : ?#?#?#?#?#?#?#?

# maj 03/12
# 1. Générer toutes les possibilités
# 2. Calculer la somme des # et filtrer celles qui n'en ont pas assez
# 3. Appliquer les regex et ne garder que les bonnes options

from itertools import product


def fill_qm_in_line(line, possible_chars):
    for product_elt_it in map(iter, product(possible_chars, repeat=line.count("?"))):
        # chaque product_elt_it est un iterator contenant le nb de caractères à remplacer.
        # La liste des itérators est l'ensemble des combinaisons possibles des caractères à remplacer
        yield "".join(c if c != "?" else next(product_elt_it) for c in line)


def get_list_of_all_possibilities(line: str) -> list[str]:
    return list(fill_qm_in_line(line, ".#"))


# TODO : inclure la fonction suivante au yield pour optim ?
def contains_enough_pounds(line: str, arr: list[int]) -> bool:
    return line.count("#") == sum(arr)


first_line_possibilities = get_list_of_all_possibilities("???.###")
first_line_filtered = [
    possib
    for possib in first_line_possibilities
    if contains_enough_pounds(possib, [1, 1, 3])
]


def is_line_regex_valid(completed_line: str, arr: list[int]) -> bool:
    reg_str = ".+#".join("{" + str(nb) + "}" for nb in arr)
    reg_str = ".*#" + reg_str + ".*"
    pattern = re.compile(reg_str)
    return pattern.match(completed_line) is not None


# print(is_line_regex_valid('#.#.###', [1, 1, 3]))
# print(is_line_regex_valid('.#...#....###.', [1, 1, 3]))
# print(is_line_regex_valid('.#.###.#.######', [1, 3, 1, 6]))
# print(is_line_regex_valid('####.#...#...', [4, 1, 1]))
# print(is_line_regex_valid('#....######..#####.', [1, 6, 5]))
# print(is_line_regex_valid('.###.##....#', [3, 2, 1]))


def take_line_and_count_good_options(line: str, arr: list[int]) -> int:
    all_line_possibilities = get_list_of_all_possibilities(line)
    first_filter = (
        possib
        for possib in all_line_possibilities
        if contains_enough_pounds(possib, arr)
    )
    second_filter = [
        possib for possib in first_filter if is_line_regex_valid(possib, arr)
    ]
    #print(second_filter)
    return len(second_filter)


def take_line_and_apply_filter_on_it_and_count(line: str, arr: list[int]) -> int:
    return len((line for line in fill_qm_in_line(line, ".#") if (contains_enough_pounds(line, arr) & is_line_regex_valid(line, arr))))

output_sum = 0
for i, line in enumerate(f_data):
    # print(line)
    output = take_line_and_count_good_options(line[0], line[1])
    # print(output)
    output_sum += output

print(output_sum)

for i in f_data_2:
    print(i)
#print(take_line_and_apply_filter_on_it_and_count("????.?????.?????.?????.?????.", [1, 1, 1, 1, 1]))

# output_sum = 0
# for i, line in enumerate(f_data_2):
#     #print(line)
#     output = take_line_and_count_good_options(line[0], line[1])
#     #print(output)
#     output_sum += output

# PART 2
# .??..??...?##. 1,1,3 - 16384 (2**14)
# Plusieurs cas
# la ligne commence
# par un . et finit par

# Idées
# - affuter la méthode de la partie 1 : 
#    - voir si certaines lignes sont contraintes, etc
#   - voir si certaines lignes sont simplifiables : par ex .??..??...?##. 1,1,3 en .??..??... 1,1
    # -> pas ouf d'après les tests
# - produire une théorie sur l'assemblage de lignes
first_line_2 = f_data_2[0]
print(first_line_2)
hash_nb = first_line_2[0].count("#")
print(hash_nb)
total_hash_nb = sum(first_line_2[1])
print(total_hash_nb)

def fill_qm_in_line_with_filter(line, possible_chars, arr):
    remaining_pounds_nb = sum(arr) - line.count("#")
    for product_elt_it in map(iter, filter(lambda tup: tup.count("#") == remaining_pounds_nb, product(possible_chars, repeat=line.count("?")))):
        # chaque product_elt_it est un iterator contenant le nb de caractères à remplacer.
        # La liste des itérators est l'ensemble des combinaisons possibles des caractères à remplacer
        yield "".join(c if c != "?" else next(product_elt_it) for c in line)


def take_filtered_line_and_apply_regex_on_it_and_count(line: str, arr: list[int]) -> int:
    return len((line for line in fill_qm_in_line_with_filter(line, ".#", arr) if is_line_regex_valid(line, arr)))


#print(take_filtered_line_and_apply_regex_on_it_and_count(first_line_2[0], first_line_2[1]))

