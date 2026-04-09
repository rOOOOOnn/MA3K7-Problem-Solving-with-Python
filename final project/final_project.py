import random
from collections import Counter
import matplotlib.pyplot as plt
import math


def merge(chain1, side1, chain2, side2):
    if side1 == "L":
        chain1 = chain1[::-1]
    else:
        chain1 = chain1[:]

    if side2 == "R":
        chain2 = chain2[::-1]
    else:
        chain2 = chain2[:]

    chain1[-1] = 0
    chain2[0] = 0
    return chain1 + chain2


def simulate_once(n):
    """
    Representation:
    - Each string starts as [1, 1].
    - 1 means a free end.
    - 0 means that part has already been tied.
    - For example, [1,1] and [1,1] can become [1,0,0,1].
    - If the two free ends of the same chain are tied, the chain becomes
      a closed loop and is recorded as a list of all 0s.
    - The function returns the final collection of loops.
    """
    chains = [[1, 1] for _ in range(n)]
    loops = []

    while chains:
        ends = []
        for i in range(len(chains)):
            ends.append((i, "L"))
            ends.append((i, "R"))

        (i1, s1), (i2, s2) = random.sample(ends, 2)

        if i1 == i2:
            chain = chains.pop(i1)
            loops.append([0] * len(chain))
        else:
            new_chain = merge(chains[i1], s1, chains[i2], s2)

            for i in sorted([i1, i2], reverse=True):
                chains.pop(i)

            chains.append(new_chain)

    return loops


def loop_count(result):
    return len(result)


def estimate_distribution(n, trials=10000):
    counts = Counter()

    for _ in range(trials):
        counts[loop_count(simulate_once(n))] += 1

    return {k: counts[k] / trials for k in range(1, n + 1)}


def exact_distribution(n):
    dist = {1: 1.0}

    for m in range(2, n + 1):
        new_dist = {}
        for l in range(1, m + 1):
            new_dist[l] = ((2 * m - 2) / (2 * m - 1)) * dist.get(l, 0.0) \
                        + (1 / (2 * m - 1)) * dist.get(l - 1, 0.0)
        dist = new_dist

    return dist


def theoretical_mean(n):
    return sum(1 / (2 * k - 1) for k in range(1, n + 1))


def theoretical_variance(n):
    return sum((1 / (2 * k - 1)) * (1 - 1 / (2 * k - 1)) for k in range(2, n + 1))


def asymptotic_mean(n):
    gamma = 0.5772156649015329
    return 0.5 * math.log(n) + math.log(2) + 0.5 * gamma


def simulate_values(n, trials=10000):
    return [loop_count(simulate_once(n)) for _ in range(trials)]


def compare_moments(ns, trials=10000):
    print(f"{'n':>5} {'Sim Mean':>12} {'Theo Mean':>12} {'Asymp Mean':>12} {'Sim Var':>12} {'Theo Var':>12}")
    print("-" * 72)

    for n in ns:
        values = simulate_values(n, trials)
        sim_mean = sum(values) / trials
        sim_var = sum((x - sim_mean) ** 2 for x in values) / trials
        theo_mean = theoretical_mean(n)
        theo_var = theoretical_variance(n)
        asymp = asymptotic_mean(n)

        print(f"{n:>5} {sim_mean:>12.6f} {theo_mean:>12.6f} {asymp:>12.6f} {sim_var:>12.6f} {theo_var:>12.6f}")


def compare_distributions(ns, trials=10000):
    print(f"{'n':>5} {'Max Abs Error':>15} {'TV Distance':>15}")
    print("-" * 40)

    for n in ns:
        sim = estimate_distribution(n, trials)
        exact = exact_distribution(n)

        max_err = max(abs(sim.get(k, 0) - exact.get(k, 0)) for k in range(1, n + 1))
        tv = 0.5 * sum(abs(sim.get(k, 0) - exact.get(k, 0)) for k in range(1, n + 1))

        print(f"{n:>5} {max_err:>15.6f} {tv:>15.6f}")


def plot_distribution(n, trials=10000, save_path=None):
    sim = estimate_distribution(n, trials)
    exact = exact_distribution(n)

    x = list(range(1, n + 1))
    y_sim = [sim[k] for k in x]
    y_exact = [exact.get(k, 0) for k in x]

    plt.figure(figsize=(8, 5))
    plt.bar(x, y_sim, alpha=0.7, label=f"Simulation ({trials} trials)")
    plt.plot(x, y_exact, marker="o", label="Exact")
    plt.xlabel("Number of loops")
    plt.ylabel("Probability")
    plt.title(f"Distribution of $L_{n}$")
    plt.xticks(x)
    plt.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)

    plt.show()


if __name__ == "__main__":
    # Small case check
    print("Exact distribution for n=5:")
    print(exact_distribution(5))
    print()

    print("Estimated distribution for n=5:")
    print(estimate_distribution(5, 10000))
    print()

    # Moment checks for larger n
    compare_moments([5, 10, 20, 50, 100], trials=10000)
    print()

    # Distribution checks for larger n
    compare_distributions([5, 10, 20, 50], trials=10000)
    print()

    # Plots
    plot_distribution(10, 10000, "dist_n10.png")
    plot_distribution(20, 10000, "dist_n20.png")
    plot_distribution(50, 10000, "dist_n50.png")