import pprint
from typing import List, Optional

class Entry(object):
    def __init__(self, val):
        self.val = val
        self.hit = False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.hit:
            return f"x{self.val}"
        else:
            return f"o{self.val}"

class Board(object):
    def __init__(self):
        self.board: List = list()
        self.winner = False


    def add_board_line(self, line):
        line = line.rstrip()
        elements = line.split(' ')

        self.board.append(list())
        for element in elements:
            if element == '':
                continue
            val = int(element)
            tmp = Entry(val)
            self.board[-1].append(tmp)

    def print_board(self):
        pprint.pprint(self.board)

    def is_winner(self):
        pass

    def hit_val(self, val) -> bool:
        for row in self.board:
            for item in row:
                if item.val == val:
                    item.hit = True
                    return True
        return False

    def check_horizontal(self) -> bool:
        for row in self.board:
            for element in row:
                if not element.hit:
                    break
            else:
                return True
        return False

    def check_vertical(self) -> bool:
        for c in range(len(self.board)):
            for r in range(len(self.board[c])):
                if not self.board[r][c].hit:
                    break
            else:
                return True

        return False

    def check_for_win(self) -> bool:
        return self.check_horizontal() or self.check_vertical()

    def sum_unmarked(self) -> int:
        total = 0
        for row in self.board:
            for element in row:
                if not element.hit:
                    total += element.val
        return total

    def set_winner(self):
        self.winner = True

class BoardsManager(object):
    def __init__(self):
        self.boards: List[Board] = list()

    def add_board(self, board: Board):
        self.boards.append(board)

    def print_boards(self):
        for idx, board in enumerate(self.boards):
            print(f"---- {idx} ---- ")
            board.print_board()

    def hit_val(self, val):
        for board in self.boards:
            if not board.winner:
                board.hit_val(val)

    def check_all_for_win(self) -> List[Board]:
        winning_boards = list()
        for board in self.boards:
            # If we already know this board is a winner, continue the game.
            if board.winner:
                continue
            if board.check_for_win():
                board.set_winner()
                winning_boards.append(board)
        return winning_boards

    def num_boards_left(self) -> int:
        count = 0
        for board in self.boards:
            if not board.winner:
                count += 1
        return count


def parse_random_numbers(rand_num_line: str):
    rand_num_line = rand_num_line.rstrip()
    num_str_vals = rand_num_line.split(',')
    return [int(x) for x in num_str_vals]


def main():
    random_numbers = list()

    boards_manager = BoardsManager()
    with open("./bingo.txt", "r") as fp:
        rand_num_line = fp.readline()
        random_numbers = parse_random_numbers(rand_num_line)
        board = Board()
        first = True
        for line in fp:
            if line.rstrip() == "" and not first:
                boards_manager.add_board(board)
                board = Board()
            elif line.rstrip() == "" and first:
                first = False
                continue
            else:
                board.add_board_line(line)

    last_random_number = 0
    last_single_winner = None
    for random_number in random_numbers:
        if boards_manager.num_boards_left() < 1:
            print("Ran out of boards.")
            break

        boards_manager.hit_val(random_number)
        winning_boards = boards_manager.check_all_for_win()

        num_winning_boards = len(winning_boards)
        if num_winning_boards > 1:
            print(f"{num_winning_boards} boards won this round.")
        elif num_winning_boards == 1:
            print("Only one winner:")
            winning_boards[0].print_board()
            last_single_winner = winning_boards[0]

        last_random_number = random_number

    unmarked_sum = last_single_winner.sum_unmarked()
    last_single_winner.print_board()
    print(f"Final value: {unmarked_sum * last_random_number}")


if __name__ == "__main__":
    main()