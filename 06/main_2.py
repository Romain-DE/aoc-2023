import pandas as pd


actual_pair = (44826981, 202107611381458)


def create_df_for_run_possibilities(time_dist_pair: tuple((int, int))) -> pd.DataFrame:
    df = pd.DataFrame({"seconds_of_loading": range(1, time_dist_pair[0])})
    df["speed_during_race"] = df["seconds_of_loading"]
    df["remaining_time"] = time_dist_pair[0] - df["seconds_of_loading"]
    df["distance"] = df["speed_during_race"] * df["remaining_time"]
    df = df[df["distance"] > time_dist_pair[1]]
    return df


print(create_df_for_run_possibilities(actual_pair))
