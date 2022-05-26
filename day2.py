
def part_1():
    depth = 0
    horiz = 0

    with open("./nav_data.txt", "r") as fp:
        lines = fp.readlines()

    for line in lines:
        tokens = line.split(' ')
        if len(tokens) < 2:
            continue

        if tokens[0] == 'forward':
            horiz += int(tokens[1])
            continue

        if tokens[0] == 'up':
            depth -= int(tokens[1])
            continue
        if tokens[0] == 'down':
            depth += int(tokens[1])
            continue


    print(f"Position {depth}, {horiz} = {depth * horiz}")

def part_2():

    aim = 0
    depth = 0
    horiz = 0

    with open("./nav_data.txt", "r") as fp:
        lines = fp.readlines()

    for line in lines:

        tokens = line.split(' ')

        if len(tokens) < 2:
            continue

        direction = tokens[0]
        val = int(tokens[1])

        if direction == 'forward':
            horiz += val
            depth += (aim * val)
            continue

        if direction == 'up':
            aim -= val
            continue

        if direction == 'down':
            aim += val
            continue

    print(f"Position {depth}, {horiz} = {depth * horiz}")


def main():
    part_2()

if __name__ == '__main__':
    main()
