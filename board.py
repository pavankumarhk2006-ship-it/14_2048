import random

SIZE = 4


class Board:
    def __init__(self):
        self.grid = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty = [
            (r, c)
            for r in range(SIZE)
            for c in range(SIZE)
            if self.grid[r][c] == 0
        ]

        if empty:
            r, c = random.choice(empty)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2

    def slide_line(self, line):
        values = [x for x in line if x != 0]

        result = []
        gained = 0
        i = 0

        while i < len(values):
            if i + 1 < len(values) and values[i] == values[i + 1]:
                merged = values[i] * 2
                result.append(merged)
                gained += merged
                i += 2
            else:
                result.append(values[i])
                i += 1

        result += [0] * (SIZE - len(result))

        return result, gained

    def move_left(self):
        changed = False
        total_gained = 0

        for r in range(SIZE):
            old = self.grid[r][:]
            new, gained = self.slide_line(old)

            self.grid[r] = new

            if old != new:
                changed = True
                total_gained += gained

        self.score += total_gained
        return changed

    def move_right(self):
        changed = False
        total_gained = 0

        for r in range(SIZE):
            old = self.grid[r][:]

            new, gained = self.slide_line(list(reversed(old)))
            new = list(reversed(new))

            self.grid[r] = new

            if old != new:
                changed = True
                total_gained += gained

        self.score += total_gained
        return changed

    def move_up(self):
        changed = False
        total_gained = 0

        for c in range(SIZE):
            old = [self.grid[r][c] for r in range(SIZE)]
            new, gained = self.slide_line(old)

            for r in range(SIZE):
                self.grid[r][c] = new[r]

            if old != new:
                changed = True
                total_gained += gained

        self.score += total_gained
        return changed

    def move_down(self):
        changed = False
        total_gained = 0

        for c in range(SIZE):
            old = [self.grid[r][c] for r in range(SIZE)]
            new, gained = self.slide_line(list(reversed(old)))
            new = list(reversed(new))

            for r in range(SIZE):
                self.grid[r][c] = new[r]

            if old != new:
                changed = True
                total_gained += gained

        self.score += total_gained
        return changed

    def can_move(self):
        if any(0 in row for row in self.grid):
            return True

        for r in range(SIZE):
            for c in range(SIZE - 1):
                if self.grid[r][c] == self.grid[r][c + 1]:
                    return True

        for r in range(SIZE - 1):
            for c in range(SIZE):
                if self.grid[r][c] == self.grid[r + 1][c]:
                    return True

        return False
