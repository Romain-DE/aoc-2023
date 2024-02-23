from copy import copy
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
    nb : int
    d: Optional["State"]
    h: Optional["State"]
    is_final: bool = False

    def __eq__(self, other: object) -> bool:
        return self.nb == other.nb

    def transition(self, letter: str) -> Optional["State"]:
        if letter == ".":
            return self.d
        elif letter == "#":
            return self.h
        else:
            return None
        
    def gen_transition(self, letter: str) -> list["State"]:
        if letter == ".":
            return [self.d]
        elif letter == "#":
            return [self.h]
        elif letter == "?":
            return [elt for elt in [self.d, self.h] if elt]
        else:
            return []


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
        states = [State() for i in range(nb_of_groups + nb_of_elts_in_groups)]
        for i, state in enumerate(states):
            state.nb = i
        return states

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
    

    def check_input_and_return_count(self, input: str) -> int :
        current_states_dict = {state.nb : 0 for state in self.states}
        current_states_dict[self.states[0].nb] = 1
        temp_state_dict = copy(current_states_dict)

        for i, char in enumerate(input):
            # print(f"[ROUND {i}]")
            # print("for char", char, "starting dict", current_states_dict)
            temp_state_dict = copy(current_states_dict)

            for state_nb in current_states_dict.keys():

                if current_states_dict[state_nb] != 0: 
                    state = self.states[state_nb]
                    new_states = state.gen_transition(char)
                    #print("going from state", state_nb, "with char", char, "to state(s)",[s.nb if s else s for s in new_states])
                    for new_state in new_states:
                        if new_state is not None: 
                            #print("dealing with dest state", new_state.nb)
                            temp_state_dict[new_state.nb] += current_states_dict[state.nb]
                            
                        #print("temp dict is now:", temp_state_dict)
                    temp_state_dict[state.nb] -= current_states_dict[state.nb]

            current_states_dict = copy(temp_state_dict)
            #print("end of ", f"[ROUND {i}] :", "TEMP dict", temp_state_dict, "Actual dict", current_states_dict)

        return current_states_dict[len(self.states) - 1]


count = 0
i = 0
for input, arr in f_data_2:
    print(input)
    print(arr)
    start_time = time.perf_counter_ns()
    i += 1
    print(i)
    count += (NFA(arr).check_input_and_return_count(input))
    end_time = time.perf_counter_ns()
    print((end_time - start_time) / 1e9)
    print("===")

print(count)
