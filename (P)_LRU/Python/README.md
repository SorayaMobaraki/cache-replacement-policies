# Least Recently Used (LRU) and Pseudo Least Recently Used (PLRU)

This directory contains documentation, reference implementations, and validation tools for two widely used cache replacement policies:

- **Least Recently Used (LRU)**
- **Pseudo Least Recently Used (PLRU)**

These policies are commonly used in modern cache hierarchies and serve as the foundation for many advanced cache replacement algorithms.

---

# Overview

When all cache ways within a set are occupied, the cache controller must decide which cache line should be replaced by a new memory block.

A **cache replacement policy** determines this decision.

LRU selects the cache line that has not been accessed for the longest period of time, while PLRU approximates the same behavior using significantly less hardware.

---

# Least Recently Used (LRU)

## Overview

Least Recently Used (LRU) is one of the most widely used cache replacement policies. It exploits **temporal locality** by assuming that data accessed recently is more likely to be accessed again.

Whenever a cache line is accessed, the replacement state is updated so that the accessed line becomes the **most recently used**, while older entries gradually become candidates for eviction.

<p align="center">
<img src="Figures/LRU.pdf" width="650">
</p>

**Figure 1.** Example illustrating the evolution of cache contents using the Least Recently Used (LRU) replacement policy.

### Advantages

- Excellent performance for workloads with temporal locality.
- Provides the exact least recently used cache line.
- Frequently used as a baseline for evaluating replacement policies.

### Limitations

- High hardware complexity.
- Requires updating replacement information after every cache access.
- Hardware cost increases with cache associativity.

---

# Pseudo Least Recently Used (PLRU)

## Overview

Pseudo Least Recently Used (PLRU) is a hardware-efficient approximation of LRU.

Instead of maintaining the exact ordering of every cache line, PLRU stores only a small number of direction bits organized as a binary tree.

This significantly reduces hardware complexity while maintaining performance close to LRU.

<p align="center">
<img src="Figures/PLRU_tree.pdf" width="500">
</p>

**Figure 2.** Binary-tree representation used by the PLRU replacement policy.

### Advantages

- Low hardware overhead.
- Efficient for highly associative caches.
- Widely implemented in commercial processors.

### Limitations

- Does not always select the true least recently used cache line.
- Replacement decisions are approximate.

---

# Repository Structure

```
(P)_LRU/

├── README.md
│
├── Figures/
│   ├── LRU.pdf
│   └── PLRU_tree.pdf
│
└── Python/
    ├── TrueLRU.py
    ├── PLRU.py
    ├── verilator_validation.py
    ├── ExtractAddress.py
    ├── L2cache.py
    ├── LRU-OrderedDict.py
    └── README.md
```

---

# Python Models

The **Python** directory contains:

- Standalone implementation of the **True LRU** algorithm.
- Standalone implementation of the **PLRU** algorithm.
- A validation framework that compares the Python models with the Chisel implementation simulated using Verilator.
- Supporting scripts for trace extraction and cache simulation.

See **`Python/README.md`** for detailed documentation of the validation framework.

---

# References

1. Mattson, R. L., Gecsei, J., Slutz, D. R., & Traiger, I. L. *Evaluation Techniques for Storage Hierarchies*. IBM Systems Journal, 1970.

2. Patterson, D. A., & Hennessy, J. L. *Computer Organization and Design: RISC-V Edition*. Morgan Kaufmann.

3. Hennessy, J. L., & Patterson, D. A. *Computer Architecture: A Quantitative Approach*. Morgan Kaufmann.

---

**Note:** All figures and illustrations in this directory were created by the author.


---

## Author

**Soraya Mobaraki**