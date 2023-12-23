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


# # 10000
#              seed        soil  fertilizer      water       light  temperature    humidity    location
# 81732  3267779837   160261436   568705787  765740342  2648249002   1671570812    24897091    31192260
# 81733  3267811052   160292651   568737002  765771557  2648280217   1671602027    24928306    31223475

# # 50000
#               seed        soil  fertilizer      water       light  temperature    humidity    location
# 408656  3267750542   160232141   568676492  765711047  2648219707   1671541517    24867796    31162965
# 408657  3267756785   160238384   568682735  765717290  2648225950   1671547760    24874039    31169208

# # 100 000 entre deux bornes :
#              seed        soil  fertilizer      water       light  temperature    humidity    location
# 17312  3267750002   160231601   568675952  765710507  2648219167   1671540977    24867256    31162425
# 17313  3267753123   160234722   568679073  765713628  2648222288   1671544098    24870377    31165546

# # 1 000 000 entre deux bornes :
#               seed        soil  fertilizer      water       light  temperature    humidity    location
# 173120  3267749516   160231115   568675466  765710021  2648218681   1671540491    24866770    31161939
# 173121  3267749828   160231427   568675778  765710333  2648218993   1671540803    24867082    31162251

#              seed       soil  fertilizer      water       light  temperature    humidity    location
# 99999  3267749828  160231427   568675778  765710333  2648218993   1671540803    24867082    31162251
# 24486  3226946696  119428295   527872646  724907201   393180862     62929170   879425717   884529426


#              seed       soil  fertilizer      water       light  temperature   humidity   location
# 38868  3267749434  160231033   568675384  765709939  2648218599   1671540409   24866688   31161857
# 38869  3267749434  160231033   568675384  765709939  2648218599   1671540409   24866688   31161857
