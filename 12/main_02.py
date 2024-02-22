from dataclasses import dataclass
from functools import cache, cached_property, lru_cache
from typing import Optional

import time

# le NFA est-il le goulot d'étranglement ? dans la suite on définit une liste de State, mais on n'utilise que le 1er
# Faut-il plutot créer une classe NFA ?
# Difficulté : si on définit un State, les enfants . et # d'un State doivent être de type Optional[State]. Comment gérer ça ?
# Forward reference with string # PEP 3107


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


f_data = Parser(day="12", filename="input.txt").f_data
f_data_2 = Parser(day="12", filename="input.txt").f_data_2


class State:
    d: Optional["State"]
    h: Optional["State"]
    is_final: bool = False

    def transition(self, letter: str):
        if letter == ".":
            return self.d
        elif letter == "#":
            return self.h
        else:
            return None


@dataclass
class NFA:
    list_of_group_size: list[int]

    def __post_init__(self):
        self.states: list[State] = self.generate()

    def generate_empty_states(self) -> list[State]:
        # Quel sera le nb de States étant donné une liste de groupes ?
        # soit N le nb de groupes
        # soit S le nb total de #
        # Alors le nb de states sera S + N
        nb_of_groups = len(self.list_of_group_size)
        nb_of_elts_in_groups = sum(self.list_of_group_size)
        return [State() for i in range(nb_of_groups + nb_of_elts_in_groups)]

    def generate(self) -> list[State]:
        # 1. Générer S + N states
        # 2. Configurer chaque state avec les règles suivantes :
        # pour chaque groupe (de taille n+1)
        # - le 1er state boucle sur lui même avec le ., et va au suivant avec le #
        # - le 2e (si non dernier) ne mène qu'au suivant avec le #
        # - ...
        # - le n+1ième
        #   - si pas dernier groupe :  mène au groupe suivant par un .
        #   - sinon : boucle sur lui même par un . et est final

        states = self.generate_empty_states()
        count = 0
        for j, nb in enumerate(self.list_of_group_size):
            for i in range(nb + 1):
                # print("will now treat elt", count)
                curr_state = states[count]
                next_state = states[count + 1] if count != len(states) - 1 else None
                if i == 0:  # 1er elt d'un groupe
                    curr_state.d = curr_state
                    curr_state.h = next_state
                elif i == nb:  # dernier elt d'un groupe
                    if j == len(self.list_of_group_size) - 1:  # cas du dernier groupe
                        curr_state.d = curr_state
                        curr_state.h = None
                        curr_state.is_final = True
                    else:
                        curr_state.d = next_state
                        curr_state.h = None
                else:
                    curr_state.d = None
                    curr_state.h = next_state

                count += 1

        return states

    def check_str_beginning(self, input: str, is_input_full: bool = False) -> bool:
        current_state = self.states[0]
        for char in input:
            next_state = current_state.transition(char)
            if next_state == None:
                return False
            current_state = next_state

        if is_input_full:
            return current_state.is_final
        else:
            return True

    def check_v2(self, input: str) -> bool:

        if (qm_count := input.count("?")) > 0:
            hash_nb = input.count("#")
            sum_of_expected_hash = sum(self.list_of_group_size)

            if hash_nb + qm_count < sum_of_expected_hash:
                return False

            qm_index = input.index("?")
            first_part = input[:qm_index]
            return self.check_str_beginning(first_part)
        
        else:
            return self.accept(input)



    def accept(self, input: str) -> bool:
        return self.check_str_beginning(input, is_input_full=True)


# nfa = NFA([3, 2, 1])
# for input in [".###.##.#...", ".###.##..#..", ".###.##....#", ".###.##...."]:
#     print(nfa.accept(input))


# nfa = NFA([2])
# for input in [".##.", "#...", "..#", "#..#"]:
#     print(nfa.accept(input))


# nfa = NFA([1, 3, 1, 6])
# for input in [".#.###.#.######"]:
#     print(nfa.accept(input))


def flatten_with_care(list_of_list) -> list:
    new_list = []

    for elt in list_of_list:
        if isinstance(elt, list):
            new_list = new_list + flatten_with_care(elt)
        else:
            new_list.append(elt)

    return new_list


def recursive_log(turn: int, *message) -> None:
    #print((turn) * "==", *message)
    pass


# Idée : améliorer la méthode .accept()
# - elle doit pouvoir gérer le "?"
#   dans ce cas, elle crée une liste [curr_state.transition(d), curr_state.transition(h)]
# - peut-être qu'il faudra changer aussi la méthode .transition(), pour qu'elle accepte un paramètre "remaining chars"


# def list_possible_arr(first_part: str, curr_char: str, last_part: str, nfa: NFA) -> int:
#     turn = len(first_part)
#     total_str = first_part + curr_char + last_part
#     qm_nb = total_str.count("?")
#     hash_nb = total_str.count("#")
#     sum_of_expected_hash = sum(nfa.list_of_group_size)

#     recursive_log(turn, "Start of fct. Args :", first_part, curr_char, last_part)

#     # Fail-fast Check
#     # return False if :
#     # 1. il n'y a plus de ?, et le nb de # est != de la somme
#     # 2. même si tous les qm etaient des #, il n'y en a pas assez pour atteindre la somme
#     # 3. il reste des QM mais que le nb est atteint

#     if qm_nb == 0:
#         if hash_nb != sum_of_expected_hash:
#             recursive_log(turn, "**Fail fast** total hash nb does not match")
#             return False
#     else:
#         if hash_nb + qm_nb < sum_of_expected_hash:
#             recursive_log(turn, "**Fail fast** not enough hash")
#             return False
#         elif hash_nb > sum_of_expected_hash:
#             recursive_log(turn, "**Fail fast** too many hash")
#             return False

#     if curr_char == "?":
#         # if not nfa.check_str_beginning(first_part):
#         #     return False

#         if (first_part + last_part).count("#") == sum_of_expected_hash:
#             recursive_log(
#                 turn, "Char is ?. Enough #. Will call :", first_part, ".", last_part
#             )
#             results = [list_possible_arr(first_part, ".", last_part, nfa)]
#         else:
#             recursive_log(turn, "Char is ?. Will call ", first_part, "[.|#]", last_part)
#             results = [
#                 list_possible_arr(first_part, ".", last_part, nfa),
#                 list_possible_arr(first_part, "#", last_part, nfa),
#             ]

#         recursive_log(turn, "results from '?' :", results)

#     elif curr_char in [".", "#"]:
#         is_input_full = last_part == ""
#         if is_input_full:  # fin de parcours
#             results = nfa.accept(first_part + curr_char)
#             recursive_log(
#                 turn,
#                 "End. Args:",
#                 first_part,
#                 curr_char,
#                 "result:",
#                 results,
#             )
#             return results

#         else:  # la recursion n'est pas finie
#             if "?" not in last_part:
#                 results = nfa.accept(total_str)
#                 recursive_log(
#                     turn,
#                     "no QM left. Is entire str correct :",
#                     results,
#                 )
#                 return results

#             else:
#                 recursive_log(
#                     turn,
#                     "On going recursion. Input is :",
#                     first_part,
#                     curr_char,
#                     last_part,
#                 )

#                 if nfa.check_str_beginning(first_part + curr_char):
#                     return list_possible_arr(
#                         first_part + curr_char, last_part[0], last_part[1:], nfa
#                     )

#                 else:
#                     recursive_log(turn, "First part incorrect")
#                     return False

#     elif curr_char == "":
#         if last_part != "":
#             recursive_log(turn, "empty current part. Will restart")
#             return list_possible_arr(first_part, last_part[0], last_part[1:], nfa)

#         else:
#             recursive_log(turn, "empty curr char, and empty last part. Will exit")
#             return None

#     recursive_log(
#         turn,
#         "End of fct. Called with",
#         first_part,
#         curr_char,
#         last_part,
#         "Result : ",
#         results,
#     )
#     return flatten_with_care(results)

nfa = NFA([3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1])


def list_possible_arr_2(input: str, nfa: NFA) -> int:
    hash_nb = input.count("#")
    sum_of_expected_hash = sum(nfa.list_of_group_size)

    if (qm_count := input.count("?")) > 0:
        qm_index = input.index("?")
        first_part, last_part = input[:qm_index], input[qm_index + 1 :]
        turn = len(first_part)
        recursive_log(turn, "Start of fct. QM remaining. Args :", input)

        if not nfa.check_str_beginning(first_part):
            recursive_log(
                turn, "first part wrong", input
            )
            return False
        
        if hash_nb + qm_count < sum_of_expected_hash:
            recursive_log(
                turn, "# nb :", hash_nb, "? nb :", qm_count, "expected sum", sum_of_expected_hash, "will be lacking # in : ", input
            )
            return False
        
        if hash_nb < sum_of_expected_hash:
            
            recursive_log(
                turn, "nb of # not reached. Trying :", first_part, "[.|#]", last_part
            )
            results = []
            add_part = ""
            if last_part.count("?") > 0:
                next_qm_index = last_part.index("?")
                add_part = last_part[:next_qm_index]
            if nfa.check_str_beginning(first_part + "." + add_part): # Ici check jusqu'au prochain QM
                # Ajouter un check : 
                results.append(list_possible_arr_2(first_part + "." + last_part, nfa))
            if nfa.check_str_beginning(first_part + "#" + add_part): # Ici check jusqu'au prochain QM
                results.append(list_possible_arr_2(first_part + "#" + last_part, nfa))
            if results == []:
                return False
            # results = [
            #     list_possible_arr_2(first_part + "." + last_part, nfa),
            #     list_possible_arr_2(first_part + "#" + last_part, nfa),
            # ]
        else:
            input_with_qm_replaced = input.replace("?", ".")
            recursive_log(turn, "nb of # reached. Trying :", input_with_qm_replaced)
            results = nfa.accept(input_with_qm_replaced)
            return results
    else:
        turn = len(input)
        recursive_log(turn, "Start of fct. Args :", input)
        results = nfa.accept(input)
        recursive_log(turn, "No QM left. Str to check :", input, "Result", results)
        return results

    recursive_log(
        turn,
        "End of fct. Called with",
        input,
        "Result : ",
        results,
    )

    return flatten_with_care(results)


def take_input_and_return_count(input: str, arr: list[int]) -> int:
    nfa = NFA(arr)
    return list_possible_arr_2(input, nfa).count(True)


#print(take_input_and_return_count("????.######..#####.", [1, 6, 5]))

# Test en 5sec avec N=4, 107s avec N=5
# line = ("???##????????#??", [7, 4])
# N = 5
# rep_line = ("?".join([line[0] for i in range(N)]), line[1] * N)
# start_time = time.perf_counter_ns()
# print(take_input_and_return_count(rep_line[0], rep_line[1]))
# end_time = time.perf_counter_ns()
# print((end_time - start_time) / 1e9)


# # intégrer la fct à la classe
# input_2500 = "????.######..#####.?????.######..#####.?????.######..#####.?????.######..#####.?????.######..#####."
# arr_2500 = [1, 6, 5, 1, 6, 5, 1, 6, 5, 1, 6, 5, 1, 6, 5]
# start_time = time.perf_counter_ns()
# # print(take_input_and_return_count(input_2500, arr_2500))
# print(list_possible_arr("", "", input_2500, nfa=NFA(arr_2500)))
# end_time = time.perf_counter_ns()
# print((end_time - start_time) / 1e9)

input_hard = "?###??????????###??????????###??????????###??????????###????????"
arr_hard = [3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1]
start_time = time.perf_counter_ns()
# print(take_input_and_return_count(input_hard, arr_hard))
list_possible_arr_2(input_hard, nfa=NFA(arr_hard))  # 33sec, puis 27, puis 24
end_time = time.perf_counter_ns()
print((end_time - start_time) / 1e9)


# count = 0
# i = 0
# for input, arr in f_data_2:
#     print(input)
#     print(arr)
#     start_time = time.perf_counter_ns()
#     i += 1
#     print(i)
#     count += take_input_and_return_count(input, arr)
#     end_time = time.perf_counter_ns()
#     print((end_time - start_time) / 1e9)
#     print("===")

# print(count)
# TODO : rajouter le check du début de str dans le fail fast ?
