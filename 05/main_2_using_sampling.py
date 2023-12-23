import pandas as pd
import numpy as np

with open("05/input.txt", "r") as file:
    data = file.read()


sections = data.split("\n\n")
seeds = [int(seed) for seed in sections[0].split(":")[1].strip().split(" ")]

# test with sampling
# seeds = [np.linspace(start=seeds[i], stop=seeds[i] + seeds[i+1], num=50000, dtype=np.int64) for i in range(0,20,2)]
# seeds = [elt for sublist in seeds for elt in sublist]
seeds = np.linspace(start=3267730000, stop=3267780000, num=100000, dtype=np.int64)


map_names = [
    "seed-to-soil map",
    "soil-to-fertilizer map",
    "fertilizer-to-water map",
    "water-to-light map",
    "light-to-temperature map",
    "temperature-to-humidity map",
    "humidity-to-location map",
]


def get_list_for_map(map_index: int) -> list[str]:
    return sections[map_index].split(":")[1].strip().split("\n")


input_map_dict = {
    map_name: [
        [int(str_int) for str_int in line_elt.split(" ")]
        for line_elt in get_list_for_map(i + 1)
    ]
    for i, map_name in enumerate(map_names)
}


def number_maps_to(map_name: str, number: int) -> int:
    map_array = np.array(input_map_dict[map_name])
    row = map_array[
        (number >= map_array[:, 1]) & (number <= map_array[:, 1] + map_array[:, 2])
    ]
    if row.size == 0:
        return number
    else:
        return row[0, 0] + number - row[0, 1]


se = pd.DataFrame({"seed": seeds})
# Idée : reprendre la solution du 1, en calculant juste les bornes [elt_0, elt_0 + elt_1, elt_2, elt_2 + elt_3, ...]
# Ensuite, voir si on peut échantilloner plus précisément quelque part


# MAJ 23/12
# 1. améliorer l'algo dans le script d'échantillonage : créer une list de rnage ? un dict de ranges ?  Comparer les perfs
# 2. Se poser et créer une vraie fonciton avec des subranges

for map in map_names:
    origin, dest = map.split(" ")[0].split("-to-")
    print(origin)
    se[dest] = se[origin].apply(lambda x: number_maps_to(map, x))


print(se.sort_values("location"))
