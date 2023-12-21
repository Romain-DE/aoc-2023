import re

with open("input.txt", "r") as file:
    data_list = file.read().split("\n")

digits_only = [re.sub("\D", "", x) for x in data_list]

correct_digits_only = [x[0] + x[-1] for x in digits_only if x != ""]
digits_as_int = [int(x) for x in correct_digits_only]
sum(digits_as_int)
