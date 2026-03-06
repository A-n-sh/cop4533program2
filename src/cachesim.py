import sys
from collections import deque, OrderedDict

def sim_fifo(k, requests):
    cache = set()
    order = deque()
    misses = 0

    for r in requests:
        if r in cache:
            continue
        misses += 1
        if len(cache) < k:
            cache.add(r)
            order.append(r)
        else:
            evicted = order.popleft()
            cache.remove(evicted)
            cache.add(r)
            order.append(r)
    return misses

def sim_lru(k, requests):
    cache = OrderedDict()
    misses = 0

    for r in requests:
        if r in cache:
            cache.move_to_end(r)
            continue
        misses += 1
        if len(cache) < k:
            cache[r] = True
        else:
            cache.popitem(last=False)
            cache[r] = True
    return misses

def sim_optff(k, requests):
    m = len(requests)
    next_use = [m] * m
    last_seen = {}
    for i in range(m - 1, -1, -1):
        if requests[i] in last_seen:
            next_use[i] = last_seen[requests[i]]
        else:
            next_use[i] = m
        last_seen[requests[i]] = i

    cache = set()
    cache_next = {}
    misses = 0

    for i, r in enumerate(requests):
        if r in cache:
            cache_next[r] = next_use[i]
            continue
        misses += 1
        if len(cache) < k:
            cache.add(r)
            cache_next[r] = next_use[i]
        else:
            evict = max(cache, key=lambda x: cache_next[x])
            cache.remove(evict)
            del cache_next[evict]
            cache.add(r)
            cache_next[r] = next_use[i]
    return misses

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <input_file>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        first_line = f.readline().split()
        k = int(first_line[0])
        m = int(first_line[1])
        requests = list(map(int, f.readline().split()))

    assert len(requests) == m, f"Expected {m} requests, got {len(requests)}"

    fifo_misses = sim_fifo(k, requests)
    lru_misses = sim_lru(k, requests)
    optff_misses = sim_optff(k, requests)

    print(f"FIFO  : {fifo_misses}")
    print(f"LRU   : {lru_misses}")
    print(f"OPTFF : {optff_misses}")

if __name__ == "__main__":
    main()