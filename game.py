from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.best_score = 0

        self.previous_grid = None
        self.previous_score = None

    def display(self):
        print("\n+------+------+------+------+")

        for row in self.board.grid:
            print(
                "|"
                + "|".join(
                    f"{x:^6}" if x else f"{' ':^6}"
                    for x in row
                )
                + "|"
            )
            print("+------+------+------+------+")

        print("Score:", self.board.score, "Best:", self.best_score)

    def move(self, key):
        moves = {
            "a": self.board.move_left,
            "d": self.board.move_right,
            "w": self.board.move_up,
            "s": self.board.move_down
        }

        if key not in moves:
            return False

        # Save state before the move
        old_grid = [row[:] for row in self.board.grid]
        old_score = self.board.score

        changed = moves[key]()

        if changed:
            # Save previous state for one-level undo
            self.previous_grid = old_grid
            self.previous_score = old_score

            # Add a new tile only after a successful move
            self.board.add_random_tile()

            # Update best score
            self.best_score = max(
                self.best_score,
                self.board.score
            )

        return changed

    def undo(self):
        if self.previous_grid is None:
            print("Nothing to undo.")
            return

        self.board.grid = [row[:] for row in self.previous_grid]
        self.board.score = self.previous_score

        # Undo can only be used once
        self.previous_grid = None
        self.previous_score = None

        print("Undo successful.")

    def run(self):
        print("2048 - W/A/S/D to move, U to undo, Q to quit.")

        while True:
            self.display()

            if any(2048 in row for row in self.board.grid):
                print("You reached 2048!")
                return

            if not self.board.can_move():
                print("No legal moves remain.")
                return

            key = input("> ").strip().lower()

            if key == "q":
                return

            if key == "u":
                self.undo()
                continue

            if key not in "wasd":
                print("Use W/A/S/D.")
                continue

            if not self.move(key):
                print("No tiles moved.")