# MAJ 15/02
# 1. Réussir à implémenter le NFA qui correspond au regex de chaque ligne
#   a. transformer le format a, b, c en une regex (c'est pas déjà fait ? )
#   b. transformer le regex en nfa
#       i. créer les états : 
#       ii. créer la fct de transition
# 2. Implémenter le "compteur", càd toutes les façons de parcourir le graphe 
# qui matchent la str de départ
#   a. 


from dataclasses import dataclass
from typing import Any, Optional

# le NFA est-il le goulot d'étranglement ? dans la suite on définit une liste de State, mais on n'utilise que le 1er
# Faut-il plutot créer une classe NFA ? 
# Difficulté : si on définit un State, les enfants . et # d'un State doivent être de type Optional[State]. Comment gérer ça ?
# Forward reference with string # PEP 3107



class State:
    name: str
    d: Optional["State"]
    h: Optional["State"]
    is_final: bool = False

    def transition(self, letter: str):
        if letter == ".":
            #print("char is .")
            return self.d
        elif letter == "#":
            #print("char is #")
            return self.h
        else :
            return None
    
    def check(self, input: str, is_input_full: bool = False) -> bool :
        current_state = self
        for char in input:
            next_state = current_state.transition(char)
            if next_state == None :
                return False
            current_state = next_state

        if is_input_full:
            return current_state.is_final
        else :
            return True
        
    def accept(self, input: str) -> bool:
        return self.check(input, is_input_full=True)

    
    def __repr__(self) -> str:
        return self.name
    
@dataclass
class NFA:
    list_of_group_size: list[int]
    
    def __post_init__(self):
        self.states: list[State] = self.generate()

    def generate_empty_states(self) -> list[State]:
        # Quel sera le nb de States étant donné un arr. ?
        # soit N le nb de groupes
        # soit S le nb total de #
        # Alors le nb de states sera S + N
        nb_of_groups = len(self.list_of_group_size)
        nb_of_elts_in_groups = sum(self.list_of_group_size)
        return [State() for i in range(nb_of_groups + nb_of_elts_in_groups)]
    
    def generate(self) -> list[State]:
        # Générer S + N states
        # Configurer chaque state avec les règles suivantes :
            # pour chaque groupe (de taille n+1)
            # - le 1er state boucle sur lui même avec le ., et va au suivant avec le #
            # - le 2e (si non dernier) ne mène qu'au suivant avec le #
            # - ...
            # - le n+1ième (si pas dernier groupe) mène au groupe suivant par un .
            # - si dernier groupe, le n+1-ième boucle sur lui même par un . et est final

        states = self.generate_empty_states()
        count = 0
        for j, nb in enumerate(self.list_of_group_size):
            for i in range(nb + 1):
                #print("will now treat elt", count)
                curr_state = states[count]
                next_state = states[count + 1] if count != len(states) - 1 else None
                if i == 0: # 1er elt d'un groupe
                    curr_state.d = curr_state
                    curr_state.h = next_state
                elif i == nb: # dernier elt d'un groupe
                    if j == len(self.list_of_group_size) - 1: # cas du dernier groupe
                        curr_state.d = curr_state
                        curr_state.h = None
                        curr_state.is_final = True
                    else :
                        curr_state.d = next_state
                        curr_state.h = None
                else : 
                    curr_state.d = None
                    curr_state.h = next_state

                count += 1
        
        return states

nfa = NFA(list_of_group_size=[3, 2, 1])
states = nfa.generate()
q0 = states[0]
print("==TEST==")
for input in [".###.##.#...", ".###.##..#..", ".###.##....#", ".###.##...."]:
    print(q0.accept(input))
print("==TEST==")
    
def generate_states(arr: list[int]) -> list[State]:
    size_of_arr = len(arr)
    sum_in_arr = sum(arr)
    list_of_states = [State() for i in range(size_of_arr + sum_in_arr)]
    for i, state in enumerate(list_of_states):
        state.name = str(i)
    
    return list_of_states

def generate_nfa(arr: list[int]) -> list[State]:
    states = generate_states(arr)
    count = 0
    for j, nb in enumerate(arr):
        for i in range(nb + 1):
            #print("will now treat elt", count)
            curr_state = states[count]
            next_state = states[count + 1] if count != len(states) - 1 else None
            if i == 0: # 1er elt d'un groupe
                curr_state.d = curr_state
                curr_state.h = next_state
            elif i == nb: # dernier elt d'un groupe
                if j == len(arr) - 1: # cas du dernier groupe
                    curr_state.d = curr_state
                    curr_state.h = None
                    curr_state.is_final = True
                else :
                    curr_state.d = next_state
                    curr_state.h = None
            else : 
                curr_state.d = None
                curr_state.h = next_state

            count += 1
    
    return states

# q0 = generate_nfa([2])[0]
# for input in [".##.", "#...", "..#", "#..#"]:
#     print(q0.accept(input))


# q0 = generate_nfa([1, 3, 1, 6])[0]
# for input in [".#.###.#.######"]:
#     print(q0.accept(input))



def flatten_with_care(list_of_list) -> list:
    new_list = []
    for elt in list_of_list:
        if isinstance(elt, list):
            new_list = new_list + flatten_with_care(elt)
        else:
            new_list.append(elt)
    
    return new_list


def recursive_log(turn: int, *message) -> None:
    pass #print((turn)*"==", *message)


# Idée : améliorer la méthode .accept()
    # elle doit pouvoir gérer le "?"
    # dans ce cas, elle crée une liste [curr_state.transition(d), curr_state.transition(h)]
    # peut-être qu'il faudra changer aussi la méthode .transition(), pour qu'elle accepte un paramètre "remaining chars"

def list_possible_arr(first_part: str, curr_char: str, last_part: str, init_state: State, arr: list[int]) -> int :
    turn = len(first_part)
    total_str = first_part + curr_char + last_part
    qm_nb = total_str.count("?")
    hash_nb = total_str.count("#")
    sum_of_expected_h = sum(arr)
    

    recursive_log(turn, "start of fct. Called with", first_part, curr_char, last_part)

    ####
    # ADD CHECK HERE #
    # return False if : 
    # 1. il n'y a plus de ?, et le nb de qm est != de la somme
    # 2. même si tous les qm etaient des #, il n'y en a pas assez pour atteindre la somme
    # 3. il reste des QM mais que le nb est atteint

    if qm_nb == 0:
        if hash_nb != sum_of_expected_h:
            recursive_log(turn, "Fail fast. total hash nb does not match")
            return False
    else :
        if hash_nb + qm_nb < sum_of_expected_h:
            recursive_log(turn, "Fail fast. not enough hash")
            return False
        elif hash_nb > sum_of_expected_h:
            return False


    if curr_char == "?":
        recursive_log(turn, "\t", "Char is ? Will create list. 1st elt is ", first_part, ".", last_part, "2d is",  first_part, "#", last_part)
        results = [
            list_possible_arr(first_part, ".", last_part, init_state, arr), 
            list_possible_arr(first_part, "#", last_part, init_state, arr)]
        recursive_log(turn, "\t", "Created list :  1st elt is ", first_part, ".", last_part, "2d is",  first_part, "#", last_part, "and the result is", results)
    elif curr_char in[".", "#"]:
        is_input_full = last_part == ""
        if is_input_full: # fin de parcours
            results = init_state.accept(first_part + curr_char)
            recursive_log(turn, "\t", "Fin de parcours.", "Les args sont", first_part + curr_char, "et le rslt", results)
            return results
                

        else : # la recursion n'est pas finie
            if "?" not in last_part:
                results = init_state.accept(first_part + curr_char + last_part)
                recursive_log(turn, "\t", "no QM left in str. Will check it entirely. Is it correct :", results)
                return results

            recursive_log(turn,"\t", "On going recursion. The input is the following :", first_part + curr_char)
            if is_first_part_correct := init_state.check(first_part + curr_char, is_input_full):
                recursive_log(turn, "\t", "first part of input correct", "Will continue and call with args ", first_part + curr_char, last_part[0], last_part[1:])
                return list_possible_arr(first_part + curr_char, last_part[0], last_part[1:], init_state, arr)
            else : 
                recursive_log(turn, "\t", "first part of input incorrect. Will return False")
                return False
            
    elif curr_char == "" :
        if last_part != "":
            recursive_log(turn, "\t", "empty current part. Will restart")
            return list_possible_arr(first_part, last_part[0], last_part[1:], init_state, arr)

        else :
            recursive_log(turn, "\t", "empty curr char, and empty last part. Will exit")
            return None
        
    recursive_log(turn, "End of fct. Called with", first_part, curr_char, last_part, "Will print result", results)
    return flatten_with_care(results)

# Ameliorer : 
# - si le nb de # restant est inférieur à la somme des nb dans l'arr, return False
# - si le nb de # et ? ..., idem
# - arrêter s'il reste des QM mais que le nb est atteint
def take_input_and_return_count(input: str, arr: list[int]) -> int:
    return list_possible_arr("", "", input, init_state=generate_nfa(arr)[0], arr=arr).count(True)

import time

print(take_input_and_return_count("????.######..#####.", [1,6,5]))

# intégrer la fct à la classe
input_2500 = "????.######..#####.?????.######..#####.?????.######..#####.?????.######..#####.?????.######..#####."
arr_2500 = [1, 6, 5, 1, 6, 5, 1, 6, 5, 1, 6, 5, 1, 6, 5]
start_time = time.perf_counter_ns()
print(take_input_and_return_count(input_2500, arr_2500))
end_time = time.perf_counter_ns()
print((end_time-start_time)/1e9)

# input_hard = "?###??????????###??????????###??????????###??????????###????????"
# arr_hard = [3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1]
# start_time = time.perf_counter_ns()
# print(take_input_and_return_count(input_hard, arr_hard))
# end_time = time.perf_counter_ns()
# print((end_time-start_time)/10e9)


# from main import f_data_2
# for input, arr in f_data_2:
#     print(input)
#     print(arr)
#     print(take_input_and_return_count(input, arr))
#     print("===")