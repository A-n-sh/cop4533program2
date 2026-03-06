# **Cache Simulator**
Simulates three cache eviction policies - FIFO, LRU, and OPTFF (Belady's Farthest-in-Future) - on a shared request sequence and reports the number of cache misses for each
## Usage
- Requires python 3
`python src/cachesim.py <input_file>`
- input\_file must match the spec provided for the project
```
k m
r1 r2 r3 ... rm
```
- Example inputs and outputs are located in examples/
- Run example 1 using `python src/cachesim.py examples/example1.in` and the expected output is in examples/example1.out
## Written Component
### Question 1: Empirical Comparison
| Input File | k | m | FIFO | LRU | OPTFF |
| ------- | --- | --- | ---- | ---- | -----|
| examples/example1.in | 3 | 64 | 28 | 32 | 21 |
| examples/example2.in | 24 | 128 | 61 | 69 | 44 |
| examples/example3.in | 8 | 128 | 42 | 37 | 20 |
- OPTFF has the fewest misses in every case
- FIFO is better than LRU in 2/3 of the test cases provided
### Question 2: Bad Sequence for LRU or FIFO
For k = 3, consider the sequence 1 2 3 4 1 2 3 4
LRU has 8 misses and 0 hits:
| Step | Request | Cache Before | Action | Cache After |
| ------ | --------- | --- | ---- | --------- |
| 1 | 1 | {} | Insert | {1} |
| 2 | 2 | {1} | Insert | {1,2} |
| 3 | 3 | {1,2} | Insert | {1,2,3} |
| 4 | 4 | {1,2,3} | Evict 1 | {2,3,4} |
| 5 | 1 | {2,3,4} | Evict 2 | {3,4,1} |
| 6 | 2 | {3,4,1} | Evict 3 | {4,1,2} |
| 7 | 3 | {4,1,2} | Evict 4 | {1,2,3} |
| 8 | 4 | {1,2,3} | Evict 1 | {2,3,4} |

LRU thrashes as it always evicts the item that is about to be needed next

OPTFF has 5 misses and 3 hits:
| Step | Request | Cache Before | Action | Cache After|
| ------- | --- | --- | ---- | ---- |
| 1 | 1 | {} | Insert | {1} |
| 2 | 2 | {1} | Insert | {1,2} |
| 3 | 3 | {1,2} | Insert | {1,2,3} |
| 4 | 4 | {1,2,3} | Evict 3 | {1,2,4} |
| 5 | 1 | {1,2,4} | Hit | {1,2,4} |
| 6 | 2 | {1,2,4} | Hit | {1,2,4} |
| 7 | 3 | {1,2,4} | Evict 1 | {2,4,3} |
| 8 | 4 | {2,4,3} | Hit | {2,4,3} |

Cycling through k + 1 = 4 distinct items causes conflict for LRU because it always evicts the least recently used item, where in a cycle happens to be the one needed next. OPTFF avoids this by looking ahead, as step 4 it evicts item 3 (farthest future use) instead of item 1, keeping the items needed at steps 5 and 6. This yields 3 hits that LRU cannot achieve.
### Question 3: Prove OPTFF is Optimal
Let A be any offline algorithm. We transform A into OPTFF one decision at a time without increasing misses.
Suppose A and OPTFF agree through step t-1, so their caches are identical. At step t both miss and must evict. OPTFF evicts item f (farthest next use), A evicts item a != f. Define A' as A but evicting f instead of a at step t.
After step t, A has f but not a, A' has a but not f. Since f has the farthest next use, a must be requested before f.

Case 1: a is requested before f. A' hits on a , A misses. If f is later requested, A' misses while A hits and the costs cancel. If f is never requested again, A' wins. Either way, misses(A') <= misses(A).

Case 2: f is requested before a. This is impossible. OPTFF chose f precisely because it has the farthest next use among all cached items, so next_use(a) <= next_use(f), meaning a must come first.

Only Case 1 applies, so misses(A') <= misses(A). Repeating at every disagreement transforms A into OPTFF without increasing misses, giving misses(OPTFF) <= misses(A) for any A.
## Authors
- Philip Baptist (UFID: )
- Ansh Gupta (UFID: 9918760)
