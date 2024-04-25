def get_ways_1(num_stairs):
    ways = []
    if num_stairs <= 0:
        ways.append([])
    else:
        for i in range(1, 4):
            if num_stairs >= i:
                result = get_ways_1(num_stairs - i)
                for j in range(len(result)):
                    result[j].insert(0, i)
                ways += result
    return ways

def get_ways_2(num_stairs):
    if num_stairs <= 0:
        return [[]]
    ways = []
    for i in range(1, 4):
        if num_stairs >= i:
            result = get_ways_2(num_stairs - i)
            for j in range(len(result)):
                result[j] = [i] + result[j]
            ways.extend(result)
    return ways

print(get_ways_1(4))
print(get_ways_2(4))

import time

start_time = time.process_time()
get_ways_1(22)
print('get_ways_1(22): %.2f seconds' % (time.process_time() - start_time))

start_time = time.process_time()
get_ways_2(22)
print('get_ways_2(22): %.2f seconds' % (time.process_time() - start_time))
