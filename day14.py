import copy
import sys
from typing import Dict, List, Tuple
import re
import time

#lookup_table = dict()

lookup_table = {
    "CH": "B",
    "HH": "N",
    "CB": "H",
    "NH": "C",
    "HB": "C",
    "HC": "B",
    "HN": "C",
    "NN": "C",
    "BH": "H",
    "NC": "B",
    "NB": "B",
    "BN": "B",
    "BB": "N",
    "BC": "B",
    "CC": "N",
    "CN": "C",
}




def add_dicts(a, b):
    final = copy.copy(b)
    for key, val in a.items():
        if key not in final:
            final[key] = val
        else:
            final[key] += val

    return final


def depth3(start_pair, depth, memo=None):

    global lookup_table

    if memo is None:
        memo = list()
        for _ in range(depth + 1):
            memo.append({})

    elif start_pair in memo[depth]:
        return memo[depth][start_pair]


    result = lookup_table[start_pair]
    next = start_pair[0] + result
    todo = result + start_pair[1]

    if depth == 1:
        return {result: 1}

    left_count = depth3(next, depth - 1, memo)
    right_count = depth3(todo, depth - 1, memo)

    memo[depth][start_pair] = add_dicts(left_count, right_count)
    if result in memo[depth][start_pair]:
        memo[depth][start_pair][result] += 1
    else:
        memo[depth][start_pair][result] = 1

    return memo[depth][start_pair]



def main():
    global lookup_table


    with open("./polymers.txt", "r") as fp:
        data = fp.read()

    data_lines = data.split("\n")
    polymer_str = data_lines[0]
    regex = re.compile("([A-Z]{2}) -> ([A-Z])")
    lookup_table = dict()
    for line in data_lines:
        m = regex.match(line)
        if m is None:
            continue
        lookup_table[m.group(1)] = m.group(2)

    print(lookup_table)


    counts = dict()
    for c in polymer_str:
        if c not in counts:
            counts[c] = 1
        else:
            counts[c] += 1

    for x in range(0, len(polymer_str) - 1):
        s = polymer_str[x:x+2]
        counts = add_dicts(depth3(s, 40), counts)


    print(counts)
    print("")
    print("Frequencies")

    max_key = max(counts, key=counts.get)
    min_key = min(counts, key=counts.get)
    print(f"Max: {max_key} = {counts[max_key]}")
    print(f"Min: {min_key} = {counts[min_key]}")
    print(f"Solution: {counts[max_key] - counts[min_key]}")

if __name__ == "__main__":
    main()