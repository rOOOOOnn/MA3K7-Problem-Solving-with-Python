import random
from fractions import Fraction

EMPTY = -1  # Sentinel value for an unfilled cell


# -------------------------
# Part 1: Create an empty n*n board
# -------------------------
def make_board(n: int):
    """Return an n-by-n board filled with EMPTY."""
    return [[EMPTY for _ in range(n)] for _ in range(n)]


def empty_cells(board):
    """Return a list of coordinates (i, j) that are still EMPTY."""
    n = len(board)
    out = []
    for i in range(n):
        for j in range(n):
            if board[i][j] == EMPTY:
                out.append((i, j))
    return out


# -------------------------
# Determinant: exact Gaussian elimination over Q (Fractions)
# -------------------------
def invariants_hold(board) -> bool:
    n = len(board)
    for j in range(n):
        if board[0][j] + board[1][j] != 1:
            return False
        if board[2][j] + board[3][j] != 1:
            return False
    return True

# -------------------------
# Part 2: Friend (Player 1) move: random 1 in any empty cell
# -------------------------
def friend_move_random(board):
    """Player 1 chooses a random empty cell and writes 1."""
    empties = empty_cells(board)
    i, j = random.choice(empties)
    board[i][j] = 1
    return (i, j)


# -------------------------
# Helper functions for the Player 0 strategy (n >= 4)
# -------------------------
def find_empty_outside_focus(board):
    """
    Return one empty cell (i, j) with i >= 4 (outside the first four rows),
    or None if no such cell exists.
    """
    n = len(board)
    for i in range(4, n):
        for j in range(n):
            if board[i][j] == EMPTY:
                return (i, j)
    return None


def scan_focus_pairs(board):
    """
    We focus on the first four rows and use two complementary row-pairs:
      (row 0, row 1) and (row 2, row 3).

    For each column j, these form two complementary cell-pairs:
      (0, j) <-> (1, j)  and  (2, j) <-> (3, j).

    This function scans those pairs and returns:
      - ("open1", pos) if there exists a pair of the form (1, EMPTY),
        where pos is the EMPTY cell that Player 0 should fill with 0;
      - ("blank", pos) if there exists a pair of the form (EMPTY, EMPTY),
        where pos is one of the empty cells (Player 0 can open a half-open pair by writing 0 there);
      - (None, None) otherwise.
    """
    n = len(board)

    # First priority: find a pair (1, EMPTY) to immediately complete with 0
    for j in range(n):
        for (r1, r2) in [(0, 1), (2, 3)]:
            a = board[r1][j]
            b = board[r2][j]
            if a == 1 and b == EMPTY:
                return ("open1", (r2, j))
            if b == 1 and a == EMPTY:
                return ("open1", (r1, j))

    # Second priority: find a completely blank pair (EMPTY, EMPTY) to open a half-open pair
    for j in range(n):
        for (r1, r2) in [(0, 1), (2, 3)]:
            a = board[r1][j]
            b = board[r2][j]
            if a == EMPTY and b == EMPTY:
                return ("blank", (r1, j))

    return (None, None)


# -------------------------
# Part 3: My move (Player 0) strategy (n >= 4), using Phase 1 / Phase 2
# -------------------------
def my_move_strategy(board):
    """
    Player 0 strategy for n >= 4:

    Phase 1 (while there exists an empty cell outside the first four rows):
      - If there is any complementary pair in the first four rows of the form (1, EMPTY),
        immediately play 0 in the EMPTY cell to complete it (sum becomes 1).
      - Otherwise, play 0 somewhere outside the first four rows (to "spend" moves safely).

    Phase 2 (once all cells outside the first four rows are filled):
      - If there is a pair (1, EMPTY), complete it by placing 0.
      - Otherwise, open a new half-open pair by placing 0 in a completely blank pair (EMPTY, EMPTY).
      This maintains the invariant that Player 1 will eventually be forced to complete the remaining half-open pair.
    """
    n = len(board)
    assert n >= 4, "This strategy is intended for n >= 4."

    outside = find_empty_outside_focus(board)

    # ----- Phase 1 -----
    if outside is not None:
        kind, pos = scan_focus_pairs(board)
        if kind == "open1":
            i, j = pos
            board[i][j] = 0
            return (i, j)

        # Otherwise, place 0 outside the focus region
        i, j = outside
        board[i][j] = 0
        return (i, j)

    # ----- Phase 2 -----
    kind, pos = scan_focus_pairs(board)
    if kind == "open1":
        i, j = pos
        board[i][j] = 0
        return (i, j)

    if kind == "blank":
        i, j = pos
        board[i][j] = 0
        return (i, j)

    # Fallback (should rarely be needed): play any remaining empty cell
    empties = empty_cells(board)
    if empties:
        i, j = empties[0]
        board[i][j] = 0
        return (i, j)
    return None


# -------------------------
# Main simulation
# -------------------------
def simulate(n: int, trials: int, seed: int = 0):
    """
    Simulate 'trials' games for a fixed n:
      - Player 0 uses my_move_strategy (n >= 4)
      - Player 1 plays randomly
    Report how many times the invariants fail (equivalently, Player 0 loses).
    """
    random.seed(seed)
    losses = 0

    for _ in range(trials):
        board = make_board(n)

        # Total moves = n^2; Player 0 moves on even turns, Player 1 on odd turns
        for t in range(n * n):
            if t % 2 == 0:
                my_move_strategy(board)
            else:
                friend_move_random(board)

        if not invariants_hold(board):
            losses += 1

    wins = trials - losses
    print(f"n={n}, trials={trials}, losses={losses}, wins={wins}, win_rate={wins/trials:.4f}")


if __name__ == "__main__":
    # Edit these parameters as needed
    simulate(n=53, trials=10000, seed=1)

'''
n=7, trials=10000, losses=0, wins=10000, win_rate=1.0000
n=10, trials=10000, losses=0, wins=10000, win_rate=1.0000
n=15, trials=10000, losses=0, wins=10000, win_rate=1.0000
n=53, trials=10000, losses=0, wins=10000, win_rate=1.0000
'''