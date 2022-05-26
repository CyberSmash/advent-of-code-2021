import statistics

def count_linear_fuel(crabs, pos):
    fuel_cost = 0
    for crab in crabs:
        fuel_cost += abs(crab - pos)
    return fuel_cost

def count_triangle_fuel(crabs, pos):
    fuel_cost = 0
    for crab in crabs:
        n = abs(crab - pos)
        fuel_cost += (n * ( n + 1 ) / 2)

    return fuel_cost

def main():
    with open("./crabs.txt", "r") as fp:
        data = fp.read()
    data = data.strip()
    data = data.split(',')
    data = [int(x) for x in data]

    data.sort()

    smallest = None
    smallest_pos = 0
    fuel_cost = 0

    print(f"Biggest crab: {max(data)}")
    #data = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]

    for x in range(max(data)):
        fuel_cost = count_triangle_fuel(data, x)
        if smallest is None:
            smallest = fuel_cost
            smallest_pos = x
        if smallest is not None and fuel_cost < smallest:
            #print(f"new smallest found: {smallest_pos} {smallest}")
            smallest = fuel_cost
            smallest_pos = x

    print(f"Smallest pos: {smallest_pos} cost: {smallest}")
    fuel_cost = count_triangle_fuel(data, 2)
    print(f"Fuel cost at pos 2: {fuel_cost}")


#print(data)
    #print(statistics.median(data))

if __name__ == "__main__":
    main()