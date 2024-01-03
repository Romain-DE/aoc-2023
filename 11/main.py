import copy
import itertools


class Parser:
    def __init__(self, day, filename="input.txt") -> None:
        self.data = self._read(day, filename)
        self.f_data = self.format_data()

    def _read(self, day, filename) -> str:
        with open(day + "/" + filename, "r") as file:
            data = file.read()
        return data

    def format_data(self) -> list[str]:
        list_of_list = self.data.split("\n")
        return list_of_list


# Etapes
# 1. Modifier l'input pour prendre en compte l'expansion de l'univers
# 2. Créer un dict avec les positions de chaque galaxie
# 3. Calculer la distance entre deux galaxie
# 4. Créer les paires
# 5. Calculer les distances pour chaque paire
# 6. Somme

f_data = Parser(day="11", filename="input.txt").f_data
f_data_part_2 = copy.copy(f_data)
data_vertical_len = len(f_data)
data_horizontal_len = len(f_data[0])


def is_row_empty_of_galaxy(f_data: list[str], row_number: str) -> bool:
    return not ("#" in f_data[row_number])


def is_column_empty_of_galaxy(f_data: list[str], col_number: int) -> bool:
    return not ("#" in [f_data[i][col_number] for i in range(data_vertical_len)])


def expand_vertically(f_data: list[str], row_nb_to_expand: int) -> list[str]:
    return (
        f_data[0:row_nb_to_expand]
        + [f_data[row_nb_to_expand]]
        + f_data[row_nb_to_expand:]
    )


def expand_horizontally(f_data: list[str], col_number_to_expand: int) -> list[str]:
    for i in range(data_vertical_len):
        f_data[i] = (
            f_data[i][0:col_number_to_expand]
            + f_data[i][col_number_to_expand]
            + f_data[i][col_number_to_expand:]
        )
    return f_data


def find_empty_rows(f_data: list[str]) -> list[str]:
    empty_row_index = []
    for row_nb in range(data_vertical_len):
        if is_row_empty_of_galaxy(f_data, row_nb):
            empty_row_index.append(row_nb)

    return empty_row_index


def find_empty_rows_and_expand(f_data: list[str]) -> list[str]:
    empty_row_index = find_empty_rows(f_data)
    for i, row_nb in enumerate(empty_row_index):
        f_data = expand_vertically(f_data, row_nb + i)
    return f_data


print(find_empty_rows_and_expand(f_data))


def find_empty_cols(f_data: list[str]) -> list[str]:
    empty_col_index = []
    for col_nb in range(data_horizontal_len):
        if is_column_empty_of_galaxy(f_data, col_nb):
            empty_col_index.append(col_nb)

    return empty_col_index


def find_empty_cols_and_expand(f_data: list[str]) -> list[str]:
    empty_col_index = find_empty_cols(f_data)
    for j, col_nb in enumerate(empty_col_index):
        f_data = expand_horizontally(f_data, col_nb + j)
    return f_data


def expand_universe(f_data) -> list[str]:
    exp_u = copy.copy(f_data)
    exp_u = find_empty_cols_and_expand(exp_u)
    exp_u = find_empty_rows_and_expand(exp_u)
    return exp_u


exp_u = expand_universe(f_data)
print(exp_u)


def find_galaxies(expanded_universe: list[str]) -> list[tuple]:
    h_size = len(expanded_universe)
    v_size = len(expanded_universe[0])
    galaxy_list = []
    for i in range(h_size):
        for j in range(v_size):
            if expanded_universe[i][j] == "#":
                galaxy_list.append((i, j))
    return galaxy_list


galaxies = find_galaxies(exp_u)


def create_pairs(list_of_galaxies: list[tuple]):
    return list(itertools.combinations(list_of_galaxies, 2))


pairs = create_pairs(galaxies)


def compute_distance(elt_1: tuple, elt_2: tuple) -> int:
    return abs(elt_1[0] - elt_2[0]) + abs(elt_1[1] - elt_2[1])


def get_distances(pair_list: list):
    return [compute_distance(elt[0], elt[1]) for elt in pair_list]


dist = get_distances(pairs)

print(dist)
print(sum(dist))  # 11675798 too high # 9521776

# Part 2
# calculer le nombre de lignes et col vides croisées
# 1. Renvoyer la liste des colonnes et lignes vides
# 2. Recréer une fonction de distance (elt_1, elt_2, facteur_multi, liste de colonnes, liste de lignes)
# 3. recalculer les paires

empty_rows = find_empty_rows(f_data_part_2)
empty_cols = find_empty_cols(f_data_part_2)


def compute_aug_dist(
    elt_1: tuple, elt_2: tuple, multip_factor: int, empty_rows: list, empty_cols: list
) -> int:
    nb_of_crossed_rows = len(
        [
            x
            for x in empty_rows
            if x in range(min([elt_1[0], elt_2[0]]), max([elt_1[0], elt_2[0]]) + 1)
        ]
    )
    nb_of_crossed_cols = len(
        [
            y
            for y in empty_cols
            if y in range(min([elt_1[1], elt_2[1]]), max([elt_1[1], elt_2[1]]) + 1)
        ]
    )

    augmented_x_dist = (multip_factor - 1) * nb_of_crossed_rows
    augmented_y_dist = (multip_factor - 1) * nb_of_crossed_cols

    return (
        abs(elt_1[0] - elt_2[0])
        + augmented_x_dist
        + abs(elt_1[1] - elt_2[1])
        + augmented_y_dist
    )


def get_aug_distances(pairs: list[tuple]) -> list[int]:
    return [
        compute_aug_dist(elt[0], elt[1], 1000000, empty_rows, empty_cols)
        for elt in pairs
    ]


unexp_galaxies = find_galaxies(f_data_part_2)
pairs_of_unexp_galaxies = create_pairs(unexp_galaxies)
dist_2 = get_aug_distances(pairs_of_unexp_galaxies)
print(sum(dist_2))
