from typing import Optional

class SegmentLayout(object):
    def __init__(self, segment):
        self.segment = segment
        self.mapping = {
            'a': 'a' in self.segment,
            'b': 'b' in self.segment,
            'c': 'c' in self.segment,
            'd': 'd' in self.segment,
            'e': 'e' in self.segment,
            'f': 'f' in self.segment,
            'g': 'g' in self.segment,
        }
        self.decoded_value : Optional[int] = None

    def length(self):
        return len(self.segment)

    def __str__(self):
        return self.segment

    def __repr__(self):
        return self.__str__()

    def print_mapping(self):
        print(f"{self.segment} = [ ")
        for key, value in self.mapping.items():
            print(f"\t{key} = {value}")
        print("]")

    def get_set(self) -> list:
        set_list = list()
        for key, val in self.mapping.items():
            if val:
                set_list.append(key)
        return set_list

    def get_set_str(self) -> str:
        s = self.get_set()
        return ''.join(s)

    def get_num_set(self):
        return len(self.get_set())

    def get_decoded_value(self) -> Optional[int]:
        return self.decoded_value

    def get_missing(self):
        missing = list()
        for key, val in self.mapping.items():
            if not val:
                missing.append(key)

        return missing

    def contains_all(self, compare_list: list) -> bool:
        return all(x in compare_list for x in self.get_set())


class SegmentLine(object):
    def __init__(self, line):
        sections = line.split(" | ")

        all_patterns = sections[0].split(" ")
        self.all_patterns = list()
        for pattern in all_patterns:
            self.all_patterns.append(SegmentLayout(pattern.strip()))

        readouts = sections[1].split(" ")
        self.readouts = list()
        for readout in readouts:
            self.readouts.append(SegmentLayout(readout))

        self.patterns_map = dict()
        self.patterns_map_r = dict()

        self.the_fifth_segment = None

    def __str__(self):
        return 'patterns: [' + ','.join([ str(pattern) for pattern in self.all_patterns ]) + ']' + ' readout: [' + ','.join([ str(readout) for readout in self.readouts ]) + ']'

    def __repr__(self):
        return self.__str__()

    def decode_readouts(self) -> int:
        final = 0
        multiplier = 1
        for readout in reversed(self.readouts):
            for key, val in self.patterns_map.items():
                if val.get_num_set() == readout.get_num_set() and all(x in readout.get_set() for x in val.get_set()):
                    print(key)
                    final += (key * multiplier)
                    multiplier *= 10

                    #print(key, end="")
                    break
        print(final)
        return final


    def set_patterns_map(self, val: int, pattern: SegmentLayout):
        self.patterns_map[val] = pattern
        self.patterns_map_r[pattern] = val

    def decode_all(self):

        self.patterns_map[1] = self.decode_one()
        self.patterns_map[7] = self.decode_seven()
        self.patterns_map[4] = self.decode_four()
        self.patterns_map[8] = self.decode_eight()
        self.patterns_map[3] = self.decode_three()
        self.patterns_map[9] = self.decode_nine()
        self.patterns_map[2] = self.decode_two()
        self.patterns_map[5] = self.decode_five()
        self.patterns_map[6] = self.decode_six()
        self.patterns_map[0] = self.decode_zero()
        for key, val in self.patterns_map.items():
            print(f" {val.get_set_str()} = {key}")


    def decode_four(self):
        for pattern in self.all_patterns:
            if pattern.get_num_set() == 4:
                pattern.decoded_value = 4
                return pattern

    def decode_eight(self):
        for pattern in self.all_patterns:
            if pattern.get_num_set() == 7:
                pattern.decoded_value = 8
                return pattern

    def decode_one(self):
        for pattern in self.all_patterns:
            if pattern.get_num_set() == 2:
                pattern.decoded_value = 1
                return pattern

    def decode_seven(self):
        for pattern in self.all_patterns:
            if pattern.get_num_set() == 3:
                pattern.decoded_value = 7
                return pattern

    def decode_three(self):
        for pattern in self.all_patterns:
            if pattern.get_num_set() == 5:
                if all(x in pattern.get_set() for x in self.patterns_map[7].get_set()):
                    pattern.decoded_value = 3
                    return pattern

    def decode_nine(self):
        for pattern in self.all_patterns:
            if pattern.get_num_set() == 6:
                if all(x in pattern.get_set() for x in self.patterns_map[4].get_set()):
                    pattern.decoded_value = 9
                    return pattern

    def decode_two(self):
        # Find the segment 'e'
        missing_segment = self.patterns_map[9].get_missing()[0]
        self.the_fifth_segment = missing_segment

        for pattern in self.all_patterns:
            if pattern.get_num_set() == 5 and missing_segment in pattern.get_set():
                pattern.decoded_value = 2
                return pattern

        return None

    def decode_five(self):
        for pattern in self.all_patterns:
            if pattern.get_num_set() == 5 and pattern.decoded_value is None:
                pattern.decoded_value = 5
                return pattern
        return None

    def decode_six(self):
        for pattern in self.all_patterns:
            if pattern.get_num_set() == 6:
                if all(x in pattern.get_set() for x in self.patterns_map[5].get_set()) and self.the_fifth_segment in pattern.get_set():
                    pattern.decoded_value = 6
                    return pattern
        return None

    def decode_zero(self):
        for pattern in self.all_patterns:
            if pattern.get_decoded_value() is None:
                pattern.decoded_value = 0
                return pattern

        return None

def main():
    with open("./segments.txt", "r") as fp:
        lines = list()
        for line in fp:
            lines.append(SegmentLine(line.strip()))
            #print(lines[-1])

        for segment in lines[-1].all_patterns:
            segment.print_mapping()
            print(segment.get_set_str())

    total = 0
    for line in lines:
        line.decode_all()
        total += line.decode_readouts()

    print(f"Total: {total}")

if __name__ == "__main__":
    main()