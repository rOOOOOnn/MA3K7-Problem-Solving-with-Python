import random
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

def run_once(base, rng):
    # Fixed-size array + active length pointer
    hat = base.copy()
    m = len(hat)
    randrange = rng.randrange

    while m > 1:
        # remove a
        i = randrange(m)
        a = hat[i]
        m -= 1
        hat[i] = hat[m]

        # remove b
        j = randrange(m)
        b = hat[j]
        m -= 1
        hat[j] = hat[m]

        # insert |a-b|
        hat[m] = a - b if a >= b else b - a
        m += 1

    return hat[0]

def simulate(trials=100_000, n=2026, seed=123):
    rng = random.Random(seed)
    base = list(range(1, n + 1))

    finals = np.empty(trials, dtype=np.int16)
    counts = np.zeros(n + 1, dtype=np.int64)

    s = 0
    s2 = 0
    for k in range(trials):
        f = run_once(base, rng)
        finals[k] = f
        counts[f] += 1
        s += f
        s2 += f * f

    mean = s / trials
    var = s2 / trials - mean * mean  # population variance
    return finals, counts, mean, var

# ---- main ----
TRIALS = 500000
N = 2026

finals, counts, mean, var = simulate(trials=TRIALS, n=N, seed=123)

# Summary stats
print("Trials:", TRIALS)
print("All odd?", bool(np.all(finals % 2 == 1)))
print("Mean:", mean)
print("Variance:", var)
print("Std:", var ** 0.5)
print("Min / Max:", int(finals.min()), int(finals.max()))
print("Unique finals observed:", int(np.count_nonzero(counts)))

# Top 10 finals by frequency
top_idx = np.argsort(counts)[-10:][::-1]
print("\nTop 10 most frequent finals (value, count, prob):")
for v in top_idx:
    c = int(counts[v])
    if c == 0:
        continue
    print(f"{int(v):4d}  {c:6d}  {c/TRIALS: .6f}")

# Head probabilities (small odd numbers)
HEAD = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]
print("\nHead probs (value: count, prob):")
for v in HEAD:
    c = int(counts[v])
    print(f"{v:4d}: {c:6d},  {c/TRIALS: .6f}")

# Histogram (linear y)
plt.figure()
plt.hist(finals, bins=60)
plt.title(f"Final value distribution ({TRIALS:,} trials)")
plt.xlabel("Final value")
plt.ylabel("Frequency")
plt.show()

# Histogram (log y) to see tail
plt.figure()
plt.hist(finals, bins=60, log=True)
plt.title(f"Final value distribution (log y) ({TRIALS:,} trials)")
plt.xlabel("Final value")
plt.ylabel("Frequency (log scale)")
plt.show()

'''
Trials: 500000
All odd? True
Mean: 338.455144
Variance: 85454.30255593924
Std: 292.3256789198295
Min / Max: 1 1957
Unique finals observed: 926

Top 10 most frequent finals (value, count, prob):
   3    2573   0.005146
   5    2519   0.005038
  11    2497   0.004994
  15    2497   0.004994
  19    2483   0.004966
  17    2474   0.004948
  27    2457   0.004914
  25    2444   0.004888
   1    2434   0.004868
   9    2426   0.004852

Head probs (value: count, prob):
   1:   2434,   0.004868
   3:   2573,   0.005146
   5:   2519,   0.005038
   7:   2397,   0.004794
   9:   2426,   0.004852
  11:   2497,   0.004994
  13:   2375,   0.004750
  15:   2497,   0.004994
  17:   2474,   0.004948
  19:   2483,   0.004966
  21:   2370,   0.004740
  23:   2380,   0.004760
  25:   2444,   0.004888
'''