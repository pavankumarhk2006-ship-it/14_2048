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

    @staticmethod
    def slide_line(line):
        # Remove zero tiles
        values = [x for x in line if x != 0]

        result = []
        i = 0

        while i < len(values):
            # Merge two equal adjacent tiles
            if (
                i + 1 < len(values)
                and values[i] == values[i + 1]
            ):
                result.append(values[i] * 2)

                # Skip both tiles that were merged.
                # This prevents chain merging.
                i += 2
            else:
                result.append(values[i])
                i += 1

        # Fill remaining positions with zeros
        result += [0] * (SIZE - len(result))

        return result

    def move_left(self):
        changed = False

        for r in range(SIZE):
            old = self.grid[r][:]

            self.grid[r] = self.slide_line(old)

            if old != self.grid[r]:
                changed = True

        return changed

    def move_right(self):
        changed = False

        for r in range(SIZE):
            old = self.grid[r][:]

            self.grid[r] = list(
                reversed(
                    self.slide_line(
                        list(reversed(old))
                    )
                )
            )

            if old != self.grid[r]:
                changed = True

        return changed

    def move_up(self):
        changed = False

        for c in range(SIZE):
            old = [
                self.grid[r][c]
                for r in range(SIZE)
            ]

            new = self.slide_line(old)

            for r in range(SIZE):
                self.grid[r][c] = new[r]

            if old != new:
                changed = True

        return changed

    def move_down(self):
        changed = False

        for c in range(SIZE):
            old = [
                self.grid[r][c]
                for r in range(SIZE)
            ]

            new = list(
                reversed(
                    self.slide_line(
                        list(reversed(old))
                    )
                )
            )

            for r in range(SIZE):
                self.grid[r][c] = new[r]

            if old != new:
                changed = True

        return changed

    def can_move(self):
        # If there is an empty cell, a move is possible
        if any(0 in row for row in self.grid):
            return True

        # Check for horizontally adjacent equal tiles
        for r in range(SIZE):
            for c in range(SIZE):
                if (
                    c + 1 < SIZE
                    and self.grid[r][c] == self.grid[r][c + 1]
                ):
                    return True

                # Check for vertically adjacent equal tiles
                if (
                    r + 1 < SIZE
                    and self.grid[r][c] == self.grid[r + 1][c]
                ):
                    return True

        return False