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


class Node(object):
    def __init__(self, data):
        self.data = data
        self.next = None
        self.repeat_forward = 1
        self.repeat_back = 0

    def insert_after(self, new_node):
        tmp = self.next
        self.next = new_node
        self.next.get_end().next = tmp

    def insert_single_after(self, new_node):
        new_node.next = self.next
        self.next = new_node


    def get_end(self):
        current = self
        while current.next is not None:
            current = current.next
        return current

class LinkedList(object):
    def __init__(self, head: Node = None):
        self.head = head

    def __str__(self):
        current = self.head
        out = ""
        while current != None:
            out += f"{current.data}" * (current.repeat_forward + current.repeat_back)
            current = current.next

        return out

    def __repr__(self):
        return self.__str__()


def insert_single_after(current_node: List, new_node: List):
    new_node[1] = current_node[1]
    current_node[1] = new_node

def str_to_linked_list(polymer: str) -> LinkedList:
    current = None
    linked_list = LinkedList()

    for p in polymer:
        if current is None:
            current = Node(p)
            linked_list.head = current
            continue
        if current.data == p:
            current.repeat_forward += 1
        else:
            current.next = Node(p)
            current = current.next

    return linked_list

def str_to_list(polymer: str) -> LinkedList:

    current = None
    head = current
    for p in polymer:
        if current is None:
            current = [p, None]
            head = current
            continue
        current[1] = [p, None]
        current = current[1]

    return head

def perform_round(polymer_linked_list: LinkedList):
    global lookup_table
    start_time = time.time()
    current = polymer_linked_list.head


    while current is not None:
        if current.next is None and current.repeat_forward > 1:
            current.insert_single_after(Node(current.data))
            current.repeat_forward -= 1
            current.insert_single_after(Node(lookup_table[current.data * 2]))
            break
        elif current.next is None and current.repeat_forward == 1:
            break

        if current.repeat_forward == 1:
            subpolymer = current.data + current.next.data
        else:
            subpolymer = current.data * 2
        result = lookup_table[subpolymer]

        if current.data == result:
            current.repeat_forward += 1
            current = current.next
        elif current.repeat_forward == 1 and current.next.data == result:
            current.next.repeat_back += 1
            current = current.next
        else:
            if current.repeat_forward > 1:
                current.repeat_forward = 1
                current.insert_single_after(Node(current.data))

            current.insert_single_after(Node(result))
            current = current.next.next


    end_time = time.time() - start_time
    print(f"Elapsed Time: {end_time}")

def perform_round_list(polymer_list: List):
    global lookup_table
    start_time = time.time()
    current = polymer_list

    while current is not None and current[1] is not None:
        subpolymer = current[0] + current[1][0]
        insert_single_after(current, [lookup_table[subpolymer], None])
        current = current[1][1]

    end_time = time.time() - start_time
    print(f"Elapsed Time: {end_time}")

def get_frequencies(polymer_linked_list: LinkedList):
    frequencies = dict()
    current = polymer_linked_list.head
    while current is not None:
        if current.data not in frequencies:
            frequencies[current.data] = 1
        else:
            frequencies[current.data] += 1
        current = current.next
    return frequencies

def print_list(start: List):
    current = start
    out_str = ""
    while current is not None:
        out_str += current[0]
        current = current[1]

    return out_str

def parse_lookup_table(table_lines: List[str]) -> Dict:
    polymer_re = re.compile("([A-Z][A-Z]) -> ([A-Z])")
    lookup_table = dict()
    for line in table_lines:

        m = polymer_re.match(line)
        if m is None:
            print(f"{line} doesn't match")
            continue
        lookup_table[m.group(1)] = m.group(2)

    print(lookup_table)
    return lookup_table

def recursive_get_new_polymer(a, b, depth, max_depth):
    if depth > max_depth:
        return a+b
    global lookup_table
    polymer = a+b
    current_idx = 0
    while current_idx < len(polymer) - 1:
        new_char = lookup_table[polymer[current_idx] + polymer[current_idx+1]]
        polymer = recursive_get_new_polymer(a, new_char, depth+1, max_depth) + polymer[current_idx:]
        print(f"Polymer: {polymer} depth: {depth}")
        current_idx += 1


    return a + new_char + b


def recursive_solution(start_string, current_depth, max_depth):
    global lookup_table
    if current_depth > max_depth:
        return start_string

    for x in range(0, len(start_string) - 1):
        pass

def at_depth(start_pair, depth):
    result = lookup_table[start_pair]
    print(f"depth {depth} val: {result}")
    if depth == 0:
        print(f"Result: {result}")
        return result
    #if depth == 1:
    #    print(f"Near Value: {result}")
    final = at_depth(start_pair[0] + result, depth - 1) + result
    if depth == 1:
        final += at_depth(result + start_pair[1], depth - 1)
        #print(f"Finsihed {start_pair[0] + result} with {final}")
        #final += at_depth(result + final[-1], depth - 1)
    #if depth == 2:
    #    final += at_depth(result + )
    return final
"""
def depth2(start_pair, depth, todo=None):
    global lookup_table
    result = lookup_table[start_pair]
    next = start_pair[0] + result
    
    if depth == 1:
        return next

    final = depth2(next, depth - 1, result + start_pair[1])
    if todo is not None:
        return final + depth2(todo, depth, None)
    else:
        return final
"""
def depth3(start_pair, depth):

    global lookup_table
    if start_pair == "NB":
        result = "B"
        next = "NB"
        todo = "BB"
        final = "NB"
        #return "NB" + depth3("BB", depth - 1)

    else:
        result = lookup_table[start_pair]
        next = start_pair[0] + result
        todo = result + start_pair[1]

    if depth == 1:
        return next

    if start_pair == "NB":
        final = "NB" + "BN" * (depth - 2)

    else:
        final = depth3(next, depth - 1)
    #final = depth3(next, depth - 1)
    if todo is not None:
        return final + depth3(todo, depth - 1)
    else:
        return final


def depth4(start_pair, depth):

    global lookup_table
    if start_pair == "NB":
        result = "B"
        next = "NB"
        todo = "BB"
        final = "NB"
        #return "NB" + depth3("BB", depth - 1)

    else:
        result = lookup_table[start_pair]
        next = start_pair[0] + result
        todo = result + start_pair[1]

    if depth == 1:
        yield next[0]
        yield next[1]
        return


    yield from depth4(next, depth - 1)

    if todo is not None:
        yield from depth4(todo, depth - 1)



def generator_test(current, end):
    if current < end:
        yield from generator_test(current + 1, end)
    if current == end:
        yield current


def main():
    global lookup_table

    for x in generator_test(5, 10):
        print(x)


    #polymer_str = "NNCB"
    polymer_str = "NNCB"
    #with open("./polymers.txt", "r") as fp:
    #    data = fp.read()

    #data_lines: List[str] = data.split("\n")
    #polymer_str = data_lines[0]
    #polymer_linked_list = str_to_linked_list(polymer_str)
    polymer_list = str_to_linked_list(polymer_str)
    #lookup_table = parse_lookup_table(data_lines[2:])

    #print(f"Polymer List: {polymer_list}")
    frequencies = {
        'B': 1,
        'N': 0,
        'H': 0,
        'C': 0,
    }
    final_str = ""
    current_str = ""
    for x in range(0, len(polymer_str) - 1):
        s = polymer_str[x:x+2]
        #current_str += f"{s}: "
        for c in depth3(s, 4):
            #print(c)
            #current_str += c
            frequencies[c] += 1
        print(f"Done .. {x}")
        #print(current_str)
        #final_str += current_str
        current_str = ""
    print("")
    print("Frequencies")
    print(frequencies)
    final_str += polymer_str[-1]

    step4_expected = "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"
    step3_expected = "NBBBCNCCNBBNBNBBCHBHHBCHB"
    if step3_expected != final_str:
        print("Does not match")
        print(step4_expected)
        #print(final_str)
        #print(len(final_str))
    else:
        print("MATCH!")

    #print(depth3("NN", 20), end="")
    #print(depth3("NC", 40), end="")
    #print(depth3("CB", 40) + "B")


    # val = f"N{middle}N"
        #middle = at_depth("CB", 3)
        #print(middle)
        #middle = at_depth(val[1])

    #for x in range(0, 4):

        #perform_round(polymer_list)
        #print(f"Finsihed round : {x+1}")
        #print(f"{polymer_list}")
    #print(f"Polymer List: {polymer_list}")

    #frequencies = get_frequencies(polymer_linked_list)
    #print(frequencies)
    #lowest_key = min(frequencies, key=frequencies.get)
    #highest_key = max(frequencies, key=frequencies.get)
    #print(f"The lowest is {lowest_key} with {frequencies[lowest_key]}")
    #print(f"The highest is {highest_key} with {frequencies[highest_key]}")

    #print(f"Solution = {frequencies[highest_key] - frequencies[lowest_key]}")

if __name__ == "__main__":
    main()