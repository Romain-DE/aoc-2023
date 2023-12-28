class Parser:
    def __init__(self) -> None:
        self.data = self._read()
        self.value_history = self.format_data()

    def _read(self) -> str:
        with open("09/input.txt", "r") as file:
            data = file.read()
        return data

    def format_data(self) -> list[list[int]]:
        list_of_raw_value_histories = self.data.split("\n")
        return [
            [int(value) for value in raw_value_histories.split(" ")]
            for raw_value_histories in list_of_raw_value_histories
        ]


def generate_list_of_differences(value_list: list[int]) -> list[int]:
    return [value_list[i + 1] - value_list[i] for i in range(len(value_list) - 1)]


def generate_new_lines_until_0(value_list: list[int], lines_of_diff=[]) -> list[int]:
    new_line = generate_list_of_differences(value_list)
    lines_of_diff.append(new_line)
    if any(elt != 0 for elt in new_line):
        return generate_new_lines_until_0(new_line, lines_of_diff)
    else:
        return lines_of_diff


def extrapolate_end_from_list_of_diff(list_of_diff: list[list[int]]) -> list[list[int]]:
    list_of_diff[-1].append(0)
    for i in range(2, len(list_of_diff) + 1):
        list_of_diff[-i].append(list_of_diff[-i][-1] + list_of_diff[-i + 1][-1])

    return list_of_diff


def extrapolate_beginning_from_list_of_diff(
    list_of_diff: list[list[int]],
) -> list[list[int]]:
    list_of_diff[-1].insert(0, 0)
    for i in range(2, len(list_of_diff) + 1):
        list_of_diff[-i].insert(0, list_of_diff[-i][0] - list_of_diff[-i + 1][0])

    return list_of_diff


def generate_end_extrapolated_lists(value_list: list[int]) -> list[list[int]]:
    list_of_diff = generate_new_lines_until_0(
        value_list=value_list, lines_of_diff=[value_list]
    )
    return extrapolate_end_from_list_of_diff(list_of_diff)


def generate_beginning_extrapolated_lists(value_list: list[int]) -> list[list[int]]:
    list_of_diff = generate_new_lines_until_0(
        value_list=value_list, lines_of_diff=[value_list]
    )
    return extrapolate_beginning_from_list_of_diff(list_of_diff)


def return_end_extrapolated_value(value_list: list[int]) -> list[list[int]]:
    return generate_end_extrapolated_lists(value_list)[0][-1]


def return_beginning_extrapolated_value(value_list: list[int]) -> list[list[int]]:
    return generate_beginning_extrapolated_lists(value_list)[0][0]


one_line = [int(i) for i in "10  13  16  21  30  45".split("  ")]
list_of_diff = generate_new_lines_until_0(one_line, [one_line])
print(list_of_diff)

print(generate_beginning_extrapolated_lists(one_line))
str_lines = ["0 3 6 9 12 15", "1 3 6 10 15 21", "10 13 16 21 30 45"]
example_lines = [[int(i) for i in ex_line.split(" ")] for ex_line in str_lines]
input_lines = Parser().value_history
print(sum([return_end_extrapolated_value(line) for line in input_lines]))
print(sum([return_beginning_extrapolated_value(line) for line in input_lines]))
