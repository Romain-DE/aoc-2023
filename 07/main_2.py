# 1. Determiner le type de main.
# 2. Pouvoir comparer deux mains
# 3. Appliquer le tri et calculer le score
from collections import Counter
import pandas as pd

with open("07/input.txt", "r") as file:
    data = file.read()


class Card:
    def __init__(self, symbol):
        self.symbol = symbol
        self.card_values = reversed("A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J".split(", "))
        self.card_values_dict = {card: i for i, card in enumerate(self.card_values)}

    def __lt__(self, other):
        return self.card_values_dict[self.symbol] < self.card_values_dict[other.symbol]

    def __eq__(self, other) -> bool:
        return self.card_values_dict[self.symbol] == self.card_values_dict[other.symbol]

    def __str__(self) -> str:
        return self.symbol


class HandType:
    def __init__(self, value) -> None:
        self.value: str = value
        self.hand_types_dict = {
            "5OK": 7,
            "4OK": 6,
            "FH": 5,
            "3OK": 4,
            "2P": 3,
            "1P": 2,
            "HC": 1,
        }

    def __lt__(self, other):
        return self.hand_types_dict[self.value] < self.hand_types_dict[other.value]

    def __eq__(self, other) -> bool:
        return self.hand_types_dict[self.value] == self.hand_types_dict[other.value]

    def __repr__(self) -> str:
        return self.value


class Hand:
    def __init__(self, value_as_str) -> None:
        self.value_as_str: str = value_as_str
        self.value: list[Card] = list(self.value_as_str)
        self.hand_type: HandType = self.__get_hand_kind__(self.value_as_str)

    def __is_same_hand_type_lt__(self, other) -> bool:
        for i in range(5):
            if Card(self.value[i]) != Card(other.value[i]):
                return Card(self.value[i]) < Card(other.value[i])
            else:
                continue

    def __get_hand_kind__(self, hand) -> HandType:
        if len(set(hand)) == 1:
            return HandType("5OK")
        else:
            count_dict = Counter(hand)
            if "J" in hand:
                del count_dict["J"]
                max_value_keys = [
                    Card(key)
                    for key, value in count_dict.items()
                    if value == max(count_dict.values())
                ]
                if len(max_value_keys) == 0:
                    replace_joker_with = "A"
                elif len(max_value_keys) == 1:
                    replace_joker_with = max(count_dict, key=count_dict.get)
                else:
                    replace_joker_with = str(
                        max(max_value_keys, key=lambda card: card.symbol)
                    )
                return self.__get_hand_kind__(
                    list(hand.replace("J", replace_joker_with))
                )

            else:
                values = list(count_dict.values())
                if 4 in values:
                    return HandType("4OK")
                elif 3 in values:
                    if 2 in values:
                        return HandType("FH")
                    else:
                        return HandType("3OK")
                elif 2 in values:
                    values.remove(2)
                    if 2 in values:
                        return HandType("2P")
                    else:
                        return HandType("1P")
                else:
                    return HandType("HC")

    def __lt__(self, other):
        return (self.hand_type < other.hand_type) | (
            (self.hand_type == other.hand_type) & (self.__is_same_hand_type_lt__(other))
        )

    def __repr__(self) -> str:
        return self.value_as_str


from operator import itemgetter

data = data.split("\n")
data = [elt.split(" ") for elt in data]
data = [(Hand(elt[0]), int(elt[1])) for elt in data]
sorted_data = sorted(data, key=itemgetter(0))
print(sorted_data)


df = pd.DataFrame(sorted_data, columns=["hand", "bet"])

df["rank"] = pd.Series(list(range(1, 1001)))
df["result"] = df["bet"] * df["rank"]
print(df)
print(sum(df["result"]))
# 251515496
