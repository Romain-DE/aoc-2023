import pandas as pd

# étapes
# 0. soit une course qui dure un temps T (int). Il y a T-2 possibilités de finir la course. Pour chacune, calculer la vitesse, et la distance parcourue.
# 1. créer une table, avec pour chaque course, les combinaisons possibles et la distance associée
# 2. réduire cette table aux combinaisons gagnantes
# 3. multiplier


with open("06/input.txt", "r") as file:
    data = file.read()

time, distance = data.split("\n")
time = [int(time) for time in time.split(":")[1].strip().split(" ") if time != ""]
distance = [
    int(dist) for dist in distance.split(":")[1].strip().split(" ") if dist != ""
]
pairs = list(zip(time, distance))
print(pairs)
print(pairs[1][0])


def create_df_for_run_possibilities(time_dist_pair: tuple((int, int))) -> pd.DataFrame:
    df = pd.DataFrame({"seconds_of_loading": range(1, time_dist_pair[0])})
    df["speed_during_race"] = df["seconds_of_loading"]
    df["remaining_time"] = time_dist_pair[0] - df["seconds_of_loading"]
    df["distance"] = df["speed_during_race"] * df["remaining_time"]
    df = df[df["distance"] > time_dist_pair[1]]
    return df


print(create_df_for_run_possibilities(pairs[0]))

count = 1
for pair in pairs:
    count = count * len(create_df_for_run_possibilities(pair))

print(count)
