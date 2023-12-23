import pandas as pd
import numpy as np


with open("05/input.txt", "r") as file:
    data = file.read()


def get_list_for_map(map_index: int) -> list[str]:
    return sections[map_index].split(":")[1].strip().split("\n")


sections = data.split("\n\n")
seeds = [int(seed) for seed in sections[0].split(":")[1].strip().split(" ")]

map_names = [
    "seed-to-soil map",
    "soil-to-fertilizer map",
    "fertilizer-to-water map",
    "water-to-light map",
    "light-to-temperature map",
    "temperature-to-humidity map",
    "humidity-to-location map",
]
input_map_dict = {
    map_name: [
        [int(str_int) for str_int in line_elt.split(" ")]
        for line_elt in get_list_for_map(i + 1)
    ]
    for i, map_name in enumerate(map_names)
}


pairs_of_seed = [
    range(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)
]
print(pairs_of_seed)
print(sum([len(pair_range) for pair_range in pairs_of_seed]))  # 2 217 452 483




def are_values_in_the_same_row(lower_bound: int, upped_bound: int, map: str) -> bool:
    df_map = pd.DataFrame(
        input_map_dict[map],
        columns=["destination", "source", "length"],
        dtype=np.int64,
    )
    filter_funct = lambda row, number: number in range(
        row["destination"], row["destination"] + row["length"]
    )
    df_map["nb_presence"] = df_map.apply(filter_funct, axis=1)
    return df_map[df_map["nb_presence"]]


def create_next_column(
    reversed_df: pd.DataFrame, current_col: str, next_col: str
) -> pd.DataFrame:
    row_of_lower_bound = which_row_is_number_enclosed_in(
        reversed_df[current_col].min(), "humidity-to-location map"
    )
    row_of_upper_bound = which_row_is_number_enclosed_in(
        reversed_df[current_col].max(), "humidity-to-location map"
    )
    if row_of_lower_bound.equals(row_of_upper_bound):
        value = row_of_lower_bound["source"].values[0]
        reversed_df[next_col] = value + pd.Series([0, N_MAX])
    else:
        print("to be implemented")

    return reversed_df

N_MAX = 1000
vect_df = pd.DataFrame({"location": range(0, N_MAX)})


# ça part dans trop de directions différentes
# - continuer sur l'intuition des N_MAX premiers entiers
