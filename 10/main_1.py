import re
from typing import Dict


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
# 0. Trouver les coord du S -> (64,79)
# 1. Créer une fonction qui renvoie les tuples (symbole, position) des éléments *accessibles* autour du S
#   a. les 4 positions
#   b. Seulement les accessibles :
#       - en haut s'il y a un 7, F ou | au dessus
#       - en bas s'il y a un J, un L ou un |
#       - à gauche s'il y a un F ou un L
#       - à droite s'il y a un 7 ou un J
# 2. Créer une fonction qui prend en arg deux tuples : (symbole de départ, position) et  (symbole suivant, position). Elle renvoie le tuple (symbole suivant, position) s'il est accessible, None sinon
# 3. Créer une fonction qui trace la trajectoire partant du S
# 4. Créer une fonction qui calcule la distance

# Notes:
# Size : 140*140
# f_data = Parser("10", "input_test_3.txt").f_data
f_data = Parser("10").f_data


def list_all_positions_around(position: tuple((int, int))) -> list[tuple((int, int))]:
    x, y = position
    size_max = len(f_data)
    # complete_list = [(x-1, y-1), (x -1, y), (x-1, y+1), (x, y+1), (x+1, y+1), (x+1, y), (x+1, y-1), (x, y-1) ]
    complete_list = [
        ((x - 1, y), "N"),
        ((x, y + 1), "E"),
        ((x + 1, y), "S"),
        ((x, y - 1), "W"),
    ]
    lambda_positive = lambda x, y: (0 <= x < size_max) & (0 <= y < size_max)
    filtered_list = [
        (elt[0], elt[1])
        for elt in complete_list
        if lambda_positive(elt[0][0], elt[0][1])
    ]
    return filtered_list


def get_all_elements_around(
    position: tuple((int, int)),
) -> list[tuple((str, tuple((int, int))))]:
    positions_around = list_all_positions_around(position)
    return [(f_data[pos[0][0]][pos[0][1]], pos[0], pos[1]) for pos in positions_around]


def criteria_list(current_elt: tuple, next_elt: tuple) -> bool:
    can_go_up = (
        (current_elt[0] in ["|", "L", "J", "S"])
        & (next_elt[2] == "N")
        & (next_elt[0] in ["7", "F", "|"])
    )
    can_go_right = (
        (current_elt[0] in ["F", "L", "-", "S"])
        & (next_elt[2] == "E")
        & (next_elt[0] in ["7", "J", "-"])
    )
    can_go_down = (
        (current_elt[0] in ["|", "7", "F", "S"])
        & (next_elt[2] == "S")
        & (next_elt[0] in ["J", "L", "|"])
    )
    can_go_left = (
        (current_elt[0] in ["J", "7", "-", "S"])
        & (next_elt[2] == "W")
        & (next_elt[0] in ["L", "F", "-"])
    )

    crits = [can_go_up, can_go_right, can_go_down, can_go_left]
    return any(crits)


def get_accessible_elt_around(position: tuple((int, int))) -> list[tuple]:
    elt_around = get_all_elements_around(position)
    return [
        elt
        for elt in elt_around
        if criteria_list(f_data[position[0]][position[1]], elt)
    ]


def get_trajectory(
    starting_point: tuple((int, int)),
) -> list[tuple((str, tuple((int, int))))]:
    trajectory_list = [("S", starting_point)]
    for elt in trajectory_list:
        around_elt = get_accessible_elt_around(elt[1])
        for elt_ar in around_elt:
            if (new_step := (elt_ar[0], elt_ar[1])) not in trajectory_list:
                trajectory_list.append(new_step)
                break
            else:
                continue

    return trajectory_list


def compute_max_dist(trajectory: list) -> int:
    traj_len_minus_start = len(trajectory) - 1
    if traj_len_minus_start % 2 == 0:
        return traj_len_minus_start - 1 / 2
    else:
        return (traj_len_minus_start + 1) / 2


# Question générale : vaut-il mieux faire des fonctions unitaire, ou qui englobent le travail précédent ?
# ça dépend un peu de si la testabilité est importante


# start_point = (64,79)
# traj = get_trajectory(start_point)
# dist = compute_max_dist(traj)
# print(traj)
# print(dist)

# Part 2
# Idée :
# 1. prendre les min et max des x et y des poitns de trajectoires. Ne considérer que ce sous-ensemble
# 2. Considérer les suites :
#   - horizontales F7, L7, FJ, LJ
#       - L7 et FJ sont eq à un |
#   - verticales (de haut en bas) : 7L, 7J, FJ, FL
#       - 7 et F sont eq à un -
#         L    J
# Simplification : traitement par ligne
# 1. considérer chaque ligne
# 2. Identifier chaque pool sur la ligne, i.e. chaque sous-ensemble d'élément contigus n'appartenant pas à la trajectoire
# 3. Pour chaque pool, vérifier l'ensemble des critères suivants :
#   - ne touche pas le bord
#   ET
#   - le pool adjacent est au bord, et la séparation est un nb impar d'eq |
#       OU
#   - le pool adjacent est à l'intérieur, et est séparé par un nb pair de | eq


def get_traj_bounds(trajectory: list[tuple]) -> list[tuple]:
    x_min = min(trajectory, key=lambda x: x[1][0])[1][0]
    y_min = min(trajectory, key=lambda x: x[1][1])[1][1]
    x_max = max(trajectory, key=lambda x: x[1][0])[1][0]
    y_max = max(trajectory, key=lambda x: x[1][1])[1][1]
    return [(x_min, y_min), (x_min, y_max), (x_max, y_max), (x_max, y_min)]


def create_line_groups(
    x_position: int, trajectory_positions: list[tuple]
) -> list[tuple]:
    list_of_groups = []

    for y_position in range(len(f_data[x_position])):
        if (x_position, y_position) not in trajectory_positions:
            if (y_position == 0) | (
                (x_position, y_position - 1) in trajectory_positions
            ):
                list_of_groups.append([(x_position, y_position)])
            else:
                if list_of_groups:
                    list_of_groups[-1].append((x_position, y_position))
                else:
                    list_of_groups.append([(x_position, y_position)])

    return list_of_groups


print(create_line_groups(6, [(elt[1][0], elt[1][1]) for elt in get_trajectory((1, 1))]))


def create_groups(trajectory: list[tuple]) -> Dict:
    trajectory_positions = [(elt[1][0], elt[1][1]) for elt in trajectory]
    dict_of_groups = {}
    for x_position in range(len(f_data)):
        dict_of_groups[x_position] = {
            str(i): {"group": group}
            for i, group in enumerate(
                create_line_groups(x_position, trajectory_positions)
            )
        }

    return dict_of_groups


def count_pipe_like_in_interval(
    end_of_group_1, beginning_of_group_2, x_position
) -> int:
    reg_str = r"(L-*7|\||F-*J|S)"
    return len(
        re.findall(
            reg_str, f_data[x_position][end_of_group_1 + 1 : beginning_of_group_2]
        )
    )


def belong_to_the_same_ensemble(
    group_1: list[tuple], group_2: list[tuple], x_position: int
) -> bool:
    return (
        count_pipe_like_in_interval(group_1[-1][1], group_2[0][1], x_position) % 2 == 0
    )


def does_group_belong_to_loop(group: list[tuple], x_position: int) -> bool:
    if min(group, key=lambda elt: elt[1])[1] == 0:
        return False
    else:
        return count_pipe_like_in_interval(-1, group[0][1], x_position) % 2 != 0


def qualify_group(dict_of_groups: Dict):
    # TODO check what follows
    for x in range(len(f_data)):
        dict_of_groups[x]["0"]["is_inside"] = does_group_belong_to_loop(
            dict_of_groups[x]["0"]["group"], x
        )
        for key, group in dict_of_groups[x].items():
            if key == "0":
                continue
            if belong_to_the_same_ensemble(
                dict_of_groups[x][str(int(key) - 1)]["group"], group["group"], x
            ):
                print("ok")
                group["is_inside"] = dict_of_groups[x][str(int(key) - 1)]["is_inside"]
            else:
                group["is_inside"] = not (
                    dict_of_groups[x][str(int(key) - 1)]["is_inside"]
                )

    return dict_of_groups


# PART 1
# start_point = (64,79)
# traj = get_trajectory(start_point)
# dist = compute_max_dist(traj)

# PART 2
start_point = (64, 79)
dict_of_groups = qualify_group(create_groups(get_trajectory(start_point)))
number_of_true = 0
for x_pos, x_dict in dict_of_groups.items():
    for group_nb, group in x_dict.items():
        if group["is_inside"]:
            number_of_true += len(group["group"])
print(dict_of_groups)
print(number_of_true)
# 331 : too low
# 340 = too higg

# print(qualify_group(dict_of_groups))
