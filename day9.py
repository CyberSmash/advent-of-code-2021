def find_low_spots(map_grid):
    low_spots = list()
    low_point_risk = list()
    for r in range(len(map_grid)):
        for c in range(len(map_grid[r])):

            max_c_index = len(map_grid) - 1
            max_r_index = len(map_grid[r]) - 1

            current_val = map_grid[r][c]
            # look up
            if r - 1 >= 0:
                if map_grid[r-1][c] <= current_val:
                    continue
            # Look down
            if r + 1 <= max_r_index:
                if map_grid[r+1][c] <= current_val:
                    continue

            # Look left
            if c - 1 >= 0:
                if map_grid[r][c-1] <= map_grid[r][c]:
                    continue
            # look right
            if c + 1 <= max_c_index:
                if map_grid[r][c+1] <= map_grid[r][c]:
                    continue

            print(f"Found low point at {r}, {c}")
            print(f"Value: {map_grid[r][c]}")
            low_point_risk.append(1+int(map_grid[r][c]))
    return low_point_risk

def main():

    with open("./heightmap.txt", "r") as fp:
        raw_file_data = fp.read()

    file_lines = raw_file_data.split()
    map_grid = list()

    for line in file_lines:
        map_grid.append(list())
        for v in line:
            map_grid[-1].append(v)

    for r_idx in range(len(map_grid)):
        print(f"{r_idx:<3}", end="")

    for r_idx, r in enumerate(map_grid):
        for c_idx, c in enumerate(r):
            if c_idx == 0:
                print(f"{r_idx:<3} | ", end="")
            print(f"{c:<3}", end="")
        print("")



    low_point_risk = find_low_spots(map_grid)
    total_risk = sum(low_point_risk)
    print(f"Torls: {total_risk}")

if __name__ == "__main__":
    main()