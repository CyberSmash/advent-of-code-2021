import os

SPAWN_TIME = 6
NEW_FISH_SPAWN_TIME = 8

class FishGroup(object):
    def __init__(self, days):
        self.days = days
        self.num_fish = 0

    def add_fish(self):
        self.num_fish += 1

    def add_multiple_fish(self, num):
        self.num_fish += num

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Days {self.days} Fish {self.num_fish}"

class FishBowl(object):
    def __init__(self):
        self.groups = list()
    def add_fish_group(self, days):
        for group in self.groups:
            if group.days == days:
                group.add_fish()
                break
        else:
            new_group = FishGroup(days)
            new_group.add_fish()
            self.groups.append(new_group)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        out = ""
        for group in self.groups:
            out += str(group) + os.linesep
        return out

    def add_new_fish(self, num):
        for group in self.groups:
            if group.days == NEW_FISH_SPAWN_TIME:
                group.num_fish += num
                break
        else:
            # We did not find a group with that number.

            new_group = FishGroup(NEW_FISH_SPAWN_TIME)
            new_group.add_multiple_fish(num)
            self.groups.append(new_group)

    def step(self):
        for group in self.groups:
            group.days -= 1

        for group in self.groups:
            if group.days == 8:
                continue
            if group.days < 0:
                self.add_new_fish(group.num_fish)
                group.days = SPAWN_TIME

        self.compact_days()

    def compact_days(self):
        for current_idx in reversed(range(len(self.groups))):
            for search_idx in reversed(range(len(self.groups))):
                if current_idx == search_idx:
                    continue

                if self.groups[current_idx].days == self.groups[search_idx].days:
                    self.groups[current_idx].add_multiple_fish(self.groups[search_idx].num_fish)
                    #print(f"removing index: {search_idx} {self.groups[search_idx].days}")
                    del self.groups[search_idx]

    def count_fish(self):
        total = 0
        for group in self.groups:
            total += group.num_fish
        return total

def main():
    with open("./fish.txt", "r") as fp:
        data = fp.read()

    # Scrub the data, make them into ints.
    data = data.strip()
    data = data.split(',')
    data = [int(x) for x in data]

    bowl = FishBowl()
    for day in data:
        bowl.add_fish_group(day)

    for x in range(0, 256):
        bowl.step()
        if x > 70:
            print(bowl)
    print(f"Total fish: {bowl.count_fish()}")


if __name__ == "__main__":
    main()