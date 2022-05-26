import pprint

def find_most_common_bit_in_column(lines, col: int, high_bias=True):
    high_count = 0
    low_count = 0

    for line in lines:
        if line[col] == 0:
            low_count += 1
        elif line[col] == 1:
            high_count += 1
    #if high_bias:
    return 1 if high_count >= low_count else 0
    #else:
    #    return 1 if high_count > low_count else 0


def filter(bits, col: int, val: int):
    new_list = list()

    for line in bits:
        if line[col] == val:
            new_list.append(line)
    return new_list


def get_gamma_and_epsilon(lines):
    gamma_bits = list()
    epsilon_bits = list()

    for x in range(0, 12):
        val = find_most_common_bit_in_column(lines, x)
        print(f"Most common in col {x} - {val}")
        gamma_bits.append(int(val != 0))
        epsilon_bits.append(int(val == 0))

    print(f"Gama Rate: {gamma_bits}")
    print(f"Epsilon Rate: {epsilon_bits}")

    gamma_val = int(''.join(str(x) for x in gamma_bits), 2)
    epsilon_val = int(''.join(str(x) for x in epsilon_bits), 2)
    print(f"Gamma val: {gamma_val}")
    print(f"Epsilon val: {epsilon_val}")

    print(f"E * G = {epsilon_val * gamma_val}")


def list_to_int(binary_list):
    return int(''.join(str(x) for x in binary_list), 2)


def get_oxygen(bits):
    bit_copy = bits.copy()
    col = 0
    while len(bit_copy) > 1:
        most_common = find_most_common_bit_in_column(bit_copy, col, high_bias=True)
        #if (len(bit_copy) <= 12):
        #    print(f"----- Before col: {col} - {most_common} ----- ")
        #    pprint.pprint(bit_copy, indent=4)
        bit_copy = filter(bit_copy, col, most_common)
        if (len(bit_copy) <= 12):
            print(f"----- After col: {col} - {most_common} ----- ")
            pprint.pprint(bit_copy, indent=4)
        #print(f"Column: {col} - {len(bit_copy)}")
        col += 1

    print(f"found {bit_copy[0]}")
    return list_to_int(bit_copy[0])

def get_co2_scrubber(bits):
    bit_copy = bits.copy()
    col = 0
    while len(bit_copy) > 1:
        most_common = find_most_common_bit_in_column(bit_copy, col, high_bias=False)
        least_common = 1 if most_common == 0 else 0
        if col >= 2:
            print(f"----- col: {col} - {least_common} / {most_common} ----- ")
            pprint.pprint(bit_copy, indent=4)
        bit_copy = filter(bit_copy, col, least_common)

        if col >= 2:
            print(f"----- After col: {col} - {least_common} / {most_common} ----- ")
            pprint.pprint(bit_copy, indent=4)

        #print(f"----- col: {col} - {least_common} ----- ")
        #pprint.pprint(bit_copy, indent=4)

        #print(f"Column: {col} - {len(bit_copy)}")
        col += 1

    print(f"found {bit_copy[0]}")
    return list_to_int(bit_copy[0])


def main():
    with open("./power_data.txt", "r") as fp:
        lines = fp.readlines()

    bits = list()
    for x in range(0, len(lines)):
        bits.append(list())
        for chr in lines[x]:
            if chr == '0':
                bits[x].append(0)
            elif chr == '1':
                bits[x].append(1)

    get_gamma_and_epsilon(bits)
    oxygen_val = get_oxygen(bits)
    print(f"Oxygen {oxygen_val}")

    co2_val = get_co2_scrubber(bits)
    print(f"Co2 val: {co2_val}")

    print(f"Final Val: {co2_val * oxygen_val}")


if __name__ == "__main__":
    main()