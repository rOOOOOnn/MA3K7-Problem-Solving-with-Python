nature_numbers = [0,1,2,3,4,5,6,7,8,9]

def number_bracelet(a, b, max_steps=500):
    if not (0 <= a < 10 and 0 <= b < 10):
        raise ValueError("Inputs must be integers in {0,...,9}.")

    seq = [a, b]
    seen_pairs = {(a, b): 0}  # pair -> index of the first element of the pair in seq

    for _ in range(max_steps):
        seq.append((seq[-1] + seq[-2]) % 10)

        pair = (seq[-2], seq[-1])
        if pair in seen_pairs:
            k = seen_pairs[pair]     # first time this pair appeared
            m = len(seq) - 2         # current index of the first element of pair
            cycle_digits = seq[k:m]  # one full period of digits
            cycle_pairs = [(cycle_digits[i], cycle_digits[(i+1) % len(cycle_digits)])
                           for i in range(len(cycle_digits))]
            return seq, cycle_digits, cycle_pairs, len(cycle_digits)

        seen_pairs[pair] = len(seq) - 2

    return seq, None, None, None


# -------------------------
# Q1: example (1,5)
# -------------------------
seq, cycle_digits, cycle_pairs, period = number_bracelet(1, 5)
print("Q1")
print("Full sequence:", seq)
print("Cycle digits:", cycle_digits)
print("Period:", period)
print()
print("-------------------------------------")
print()

# -------------------------
# Q2: count distinct bracelets
# -------------------------
def canonical_cycle(cycle_pairs):
    """Identify a bracelet up to rotation (not reflection)."""
    # rotate so the lexicographically smallest pair comes first
    n = len(cycle_pairs)
    best = None
    for shift in range(n):
        rot = tuple(cycle_pairs[shift:] + cycle_pairs[:shift])
        if best is None or rot < best:
            best = rot
    return best

bracelets = {}  # key (canonical cycle) -> (length, representative start pair)

for i in nature_numbers:
    for j in nature_numbers:
        _, _, cp, L = number_bracelet(i, j)
        key = canonical_cycle(cp)     # classification by cycle identity, not by length
        if key not in bracelets:
            bracelets[key] = (L, (i, j))

print("Q2")
print("Number of different bracelets:", len(bracelets))

# Lengths are only a summary statistic, not an identifier:
lengths = sorted([v[0] for v in bracelets.values()], reverse=True)
print("Bracelet lengths (summary only):", lengths)

print("Number of different bracelets:", len(bracelets))

# Sort bracelets by length (desc), then by representative start pair
items = sorted(bracelets.items(), key=lambda kv: (-kv[1][0], kv[1][1]))

PRINT_PAIRS = False  # set True if you also want to print cycle_pairs

for idx, (key, (L, rep)) in enumerate(items, start=1):
    # recompute the cycle from the representative start so we can print it
    _, cycle_digits, cycle_pairs, _ = number_bracelet(rep[0], rep[1])

    print(f"\nBracelet #{idx}")
    print(f"  Length: {L}")
    print(f"  Representative start pair: {rep}")
    print(f"  Cycle digits: {cycle_digits}")

    if PRINT_PAIRS:
        print(f"  Cycle pairs: {cycle_pairs}")

# sanity check (should be 100 if you're counting over 0..9 x 0..9)
print("\nSanity check (sum of cycle lengths):", sum(v[0] for v in bracelets.values()))

'''
OUTPUT

Q1
Full sequence: [1, 5, 6, 1, 7, 8, 5, 3, 8, 1, 9, 0, 9, 9, 8, 7, 5, 2, 7, 9, 6, 5, 1, 6, 7, 3, 0, 3, 3, 6, 9, 5, 4, 9, 3, 2, 5, 7, 2, 9, 1, 0, 1, 1, 2, 3, 5, 8, 3, 1, 4, 5, 9, 4, 3, 7, 0, 7, 7, 4, 1, 5]
Cycle digits: [1, 5, 6, 1, 7, 8, 5, 3, 8, 1, 9, 0, 9, 9, 8, 7, 5, 2, 7, 9, 6, 5, 1, 6, 7, 3, 0, 3, 3, 6, 9, 5, 4, 9, 3, 2, 5, 7, 2, 9, 1, 0, 1, 1, 2, 3, 5, 8, 3, 1, 4, 5, 9, 4, 3, 7, 0, 7, 7, 4]
Period: 60

-------------------------------------

Q2
Number of different bracelets: 6
Bracelet lengths (summary only): [60, 20, 12, 4, 3, 1]
Number of different bracelets: 6

Bracelet #1
  Length: 60
  Representative start pair: (0, 1)
  Cycle digits: [0, 1, 1, 2, 3, 5, 8, 3, 1, 4, 5, 9, 4, 3, 7, 0, 7, 7, 4, 1, 5, 6, 1, 7, 8, 5, 3, 8, 1, 9, 0, 9, 9, 8, 7, 5, 2, 7, 9, 6, 5, 1, 6, 7, 3, 0, 3, 3, 6, 9, 5, 4, 9, 3, 2, 5, 7, 2, 9, 1]

Bracelet #2
  Length: 20
  Representative start pair: (0, 2)
  Cycle digits: [0, 2, 2, 4, 6, 0, 6, 6, 2, 8, 0, 8, 8, 6, 4, 0, 4, 4, 8, 2]

Bracelet #3
  Length: 12
  Representative start pair: (1, 3)
  Cycle digits: [1, 3, 4, 7, 1, 8, 9, 7, 6, 3, 9, 2]

Bracelet #4
  Length: 4
  Representative start pair: (2, 6)
  Cycle digits: [2, 6, 8, 4]

Bracelet #5
  Length: 3
  Representative start pair: (0, 5)
  Cycle digits: [0, 5, 5]

Bracelet #6
  Length: 1
  Representative start pair: (0, 0)
  Cycle digits: [0]

Sanity check (sum of cycle lengths): 100
'''