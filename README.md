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
- examples/example1.in has k=3 and OPTFF yields 21 misses compared to FIFO's 28 and LRU's 32.
- OPTFF is an optimal algorithm at minimizing the number of misses, so LRU or FIFO can do no better than OPTFF. In this particular case, OPTFF performs strictly better than both LRU and FIFO.

