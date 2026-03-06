# **Cache Simulator**
Simulates three cache eviction policies - FIFO, LRU, and OPTFF (Belady's Farther-in-Future) - on a shared request sequence and reports the number of cache misses for each
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
### Question 3:
Let OPTFF solution be O, and any other arbitrary sequence be A.
Consider the first difference between O and A, which occurs at request i which requests item d.
Let the evicted item from O be b, and from A be a.
Case 1, if a=b, then this is not a difference between O and A. 
Case 2, If d is already present, then O does not evict any entries and A could not reduce the number of evictions by bringing a duplicate entry into the cache.
Case 3, if a!=b, then let the first step after this where O and A differ be j which requests item c.
It is impossible for c=a because the OPTFF solution O by definition evicts the entry which will not be request for the longest time, otherwise c=a=b.
If c=b, then O must evict some entry d since it evicted b. 
If d=a, then O and A now match. If d!=a, then A can arbitrarily evict d and insert a, making O and A match.
If d!=a and d!=b, then A can evict b, making O and A match.
This comparsion can recurse, and in every case O has no more evictions than the sequence A.
## Authors
- Philip Baptist
- Ansh Gupta
