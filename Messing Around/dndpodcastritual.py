import random

from tqdm import trange
import numpy as np

trials = 1000000

success_req = 10
fail_req = 3

members = 2

d20 = random.Random()

def roll():
    return d20.randint(1, 20)

def test(advantage):
    success = 0
    fails = np.repeat([0], members)
    cur_member = 0
    while success < success_req and not np.all(np.greater_equal(fails, fail_req)):
        res = roll()
        if advantage:
            res = max(res, roll())
        if res == 1 or (res == 5 and advantage):
            fails[cur_member] += 2
        elif res < success_req:
            fails[cur_member] += 1
        else:
            success += 1
        cur_member = cur_member + 1 if cur_member + 1 < members else 0
        # Continue cycling until non dead member
        while fails[cur_member] >= fail_req and not np.all(np.greater_equal(fails, fail_req)) :
            cur_member = cur_member + 1 if cur_member + 1 < members else 0
    if success == success_req:
        return (True, np.count_nonzero(np.greater_equal(fails, fail_req)))
    elif np.count_nonzero(np.greater_equal(fails, fail_req)) == members:
        return (False, members)
    else:
        raise AssertionError("Number of dead members does not equal total members on a failed ritual. Check for bugs.")
            
nonadvantage_successes = np.repeat([0], members)
advantage_successes = np.repeat([0], members)

for _ in trange(trials):
    # res, dead = test(False)
    # if res:
    #     nonadvantage_successes[dead] += 1
    resa, deada = test(True)
    resn, deadn = test(False)
    if resa:
        advantage_successes[deada] += 1
    if resn:
        nonadvantage_successes[deadn] += 1

print("Results: ")
print(f"  Non Advantage:")
for i in range(members):
    print(f"    Successes ({i} dead): {nonadvantage_successes[i]}")
print(f"    Fails: {trials - np.sum(nonadvantage_successes)}")
print(f"  Success ratio: {sum(nonadvantage_successes)/trials * 100}%")
print(f"  Advantage:")
for i in range(members):
    print(f"    Successes ({i} dead): {advantage_successes[i]}")
print(f"    Fails: {trials - np.sum(advantage_successes)}")
print(f"  Success ratio: {sum(advantage_successes)/trials * 100}%")