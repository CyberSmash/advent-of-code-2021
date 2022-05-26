
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

    def insert_after(self, new_node):
        tmp = self.next
        self.next = new_node
        self.next.get_end().next = tmp

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
            out += current.data
            current = current.next

        return out

    def __repr__(self):
        return self.__str__()

def str_to_linked_list(polymer: str) -> LinkedList:
    current = None
    linked_list = LinkedList()
    for p in polymer:
        if current is None:
            current = Node(p)
            linked_list.head = current
            continue
        current.next = Node(p)
        current = current.next

    return linked_list

def perform_round(polymer_linked_list: LinkedList):
    current = polymer_linked_list.head
    while current is not None and current.next is not None:
        next = current.next
        subpolymer = current.data + next.data
        new_node = Node(lookup_table[subpolymer])
        current.insert_after(new_node)
        current = next

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


def main():
    polymer_str = "NNCB"

    polymer_linked_list = str_to_linked_list(polymer_str)
    current = polymer_linked_list.head
    while current is not None:
        print(current.data)
        current = current.next
    print("")

    for x in range(0, 10):
        perform_round(polymer_linked_list)
        print(f"{polymer_linked_list}")
    frequencies = get_frequencies(polymer_linked_list)
    print(frequencies)
    lowest_key = min(frequencies, key=frequencies.get)
    highest_key = max(frequencies, key=frequencies.get)
    print(f"The lowest is {lowest_key} with {frequencies[lowest_key]}")
    print(f"The highest is {highest_key} with {frequencies[highest_key]}")

    print(f"Solution = {frequencies[highest_key] - frequencies[lowest_key]}")

if __name__ == "__main__":
    main()