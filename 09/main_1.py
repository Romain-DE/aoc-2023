
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
        return [[int(value) for value in raw_value_histories.split(" ")] for raw_value_histories in list_of_raw_value_histories]


print(Parser().value_history)

def generate_list_of_differences(value_list : list[int]) -> list[int]:
    return [value_list[i + 1] - value_list[i] for i in range(len(value_list) - 1)]

one_line = [int(i) for i in "0 3 6 9 12 15".split(" ")]

print(generate_list_of_differences(one_line))
print(generate_list_of_differences([3, 3, 3, 3, 3]))