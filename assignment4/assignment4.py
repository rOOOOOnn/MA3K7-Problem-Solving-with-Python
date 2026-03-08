import random

def random_step():
    # Return a random move of 1 or 2
    return random.choice([1, 2])

def single_trial(target=25):
    # Start from 1 and stop once reaching or passing target
    position = 1
    for _ in range(25):
        position += random_step()
        if position >= target:
            break
    return position == target

def estimate_probability(n_trials=1000000, target=25):
    # Run many trials and estimate hit probability
    hits = 0
    for _ in range(n_trials):
        if single_trial(target):
            hits += 1
    return hits / n_trials

prob = estimate_probability(1000000, 25)
print("Estimated probability:", prob)


'''
Estimated probability: 0.666344
Estimated probability: 0.667214
Estimated probability: 0.667154
Estimated probability: 0.666902
'''