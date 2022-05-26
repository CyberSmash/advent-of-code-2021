import queue

open_brackets = ['{', '[', '(', '<']
closed_brackets = ['}', ']', ')', '>']

invalid_scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

fix_scores = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def get_matching(open_bracket):
    idx = open_brackets.index(open_bracket)
    return closed_brackets[idx]


def find_invalid(line) -> str:
    q = queue.LifoQueue()
    for c in line:
        if c in open_brackets:
            q.put(c)
        if c in closed_brackets:
            if q.empty():
                print(f"Invalid bracket: {c}", end="")
                return c
            prev = q.get()
            expected = get_matching(prev)
            if c != expected:
                print(f"Invalid bracket: {c}", end="")
                return c
    return '!'


def complete_line(line):
    q = queue.LifoQueue()

    for c in line:
        if c in open_brackets:
            q.put(c)
        elif c in closed_brackets:
            if q.empty():
                print(f"Something's wrong. This line is invalid, and not just incomplete")
                return "?"
            prev = q.get()
            expected = get_matching(prev)
            if c != expected:
                print(f"Something's wrong. This line is invalid and not just incomplete.")
                return "?"

    # Now we have a queue full of open brackets that are unclosed. Return a list of closed brackets
    ret = list()
    while not q.empty():
        ret.append(get_matching(q.get()))

    return ret

def score_result(result) -> int:
    total_score = 0

    for r in result:
        total_score *= 5
        total_score += fix_scores[r]

    return total_score

def main():
    invalid_score = 0
    all_data = None
    incomplete_scores = list()

    with open("./brackets.txt", "r") as fp:
        all_data = fp.read()

    all_lines = all_data.split()

    incomplete_lines = list()
    for idx, line in enumerate(all_lines):
        res = find_invalid(line)
        if res != '!':
            print(f" on line {idx}")
            invalid_score += invalid_scores[res]
        else:
            incomplete_lines.append(line)


    print(f"Invalid Score: {invalid_score}")

    for incomplete_line in incomplete_lines:
        result = complete_line(incomplete_line)
        incomplete_scores.append(score_result(result))
        print(f"Score: {incomplete_scores[-1]}")
    print(f"Answer: {len(incomplete_scores)}")
    incomplete_scores.sort(reverse=True)
    for score in incomplete_scores:
        print(score)

    print(f"Answer: {incomplete_scores[len(incomplete_scores) // 2]}")

if __name__ == "__main__":
    main()