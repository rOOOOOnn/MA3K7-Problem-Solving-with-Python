import random

EMPTY = -1  # empty cell


# ---- board ----
def make_board(n: int):
    """n x n board."""
    return [[EMPTY for _ in range(n)] for _ in range(n)]


def empty_cells(board):
    """All empty positions."""
    out = []
    for i, row in enumerate(board):
        for j, v in enumerate(row):
            if v == EMPTY:
                out.append((i, j))
    return out


# ---- end-game invariant (proof) ----
def invariants_hold(board) -> bool:
    """Check R0+R1=u and R2+R3=u (end state)."""
    n = len(board)
    if n < 4:
        return False
    for j in range(n):
        a, b = board[0][j], board[1][j]
        c, d = board[2][j], board[3][j]
        if a == EMPTY or b == EMPTY or c == EMPTY or d == EMPTY:
            return False
        if a + b != 1 or c + d != 1:
            return False
    return True


# ---- Player 1 (random) ----
def friend_move_random(board):
    """Random 1."""
    i, j = random.choice(empty_cells(board))
    board[i][j] = 1
    return (i, j)


# ---- Player 0 helpers (focus rows 0..3) ----
def find_empty_outside_focus(board):
    """Any empty cell with row >= 4."""
    n = len(board)
    for i in range(4, n):
        for j in range(n):
            if board[i][j] == EMPTY:
                return (i, j)
    return None


def scan_focus_pairs(board):
    """Find (1,EMPTY) first; else (EMPTY,EMPTY)."""
    n = len(board)

    # close (1, EMPTY)
    for j in range(n):
        for r1, r2 in ((0, 1), (2, 3)):
            a, b = board[r1][j], board[r2][j]
            if a == 1 and b == EMPTY:
                return ("open1", (r2, j))
            if b == 1 and a == EMPTY:
                return ("open1", (r1, j))

    # open (EMPTY, EMPTY)
    for j in range(n):
        for r1, r2 in ((0, 1), (2, 3)):
            if board[r1][j] == EMPTY and board[r2][j] == EMPTY:
                return ("blank", (r1, j))

    return (None, None)


# ---- Player 0 strategy (n >= 4) ----
def my_move_strategy(board):
    """Phase1: spend outside. Phase2: maintain one half-open."""
    n = len(board)
    assert n >= 4

    outside = find_empty_outside_focus(board)

    # Phase 1: outside available
    if outside is not None:
        kind, pos = scan_focus_pairs(board)
        if kind == "open1":
            i, j = pos
            board[i][j] = 0
            return (i, j)
        i, j = outside
        board[i][j] = 0
        return (i, j)

    # Phase 2: outside full
    kind, pos = scan_focus_pairs(board)
    if kind in ("open1", "blank"):
        i, j = pos
        board[i][j] = 0
        return (i, j)

    # fallback (should not happen)
    i, j = empty_cells(board)[0]
    board[i][j] = 0
    return (i, j)


# ---- simulation ----
def simulate(n: int, trials: int, seed: int = 1):
    """Run trials; count invariant failures."""
    random.seed(seed)
    losses = 0

    for _ in range(trials):
        board = make_board(n)

        for t in range(n * n):
            if t % 2 == 0:
                my_move_strategy(board)
            else:
                friend_move_random(board)

        # check once per game
        if not invariants_hold(board):
            losses += 1

    wins = trials - losses
    print(f"n={n}, trials={trials}, seed={seed}, losses={losses}, wins={wins}, win_rate={wins/trials:.4f}")


if __name__ == "__main__":
    simulate(n=53, trials=10000, seed=1)


'''
n=7, trials=10000, losses=0, wins=10000, win_rate=1.0000
n=10, trials=10000, losses=0, wins=10000, win_rate=1.0000
n=15, trials=10000, losses=0, wins=10000, win_rate=1.0000
n=53, trials=10000, losses=0, wins=10000, win_rate=1.0000
'''