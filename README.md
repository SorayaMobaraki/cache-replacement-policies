
# Cache Replacement Policies

A collection of reference implementations and documentation for modern cache replacement policies.

This repository provides software implementations of several cache replacement algorithms together with supporting documentation and validation code. It is intended for students, researchers, and computer architects interested in cache memory systems.

---

## Repository Contents

The repository currently includes implementations of the following cache replacement policies:

- **Least Recently Used (LRU)**
- **Pseudo Least Recently Used (PLRU)**
- **Signature-based Hit Predictor (SHiP)**
- **Hawkeye**

Depending on the policy, implementations may be available in Python and/or C++.

---

## Repository Structure

```
cache-replacement-policies/

├── lru and plru/
│   ├── python/
│   ├── docs/
│   └── README.md
│
├── ship/
│   ├── HLS/
│   ├── docs/
│   └── README.md
│
├── hawkeye/
│   ├── python/
│   ├── cpp/
│   ├── docs/
│   └── README.md
│
└── README.md
```

---

## Objectives

- Provide clean reference implementations of cache replacement policies.
- Document the design principles behind each algorithm.
- Support algorithm comparison and experimentation.
- Serve as a learning resource for cache memory systems.

---

## Policies

### LRU (Least Recently Used)

A stack-based replacement policy that always evicts the cache block that has not been accessed for the longest time.

---

### PLRU (Pseudo Least Recently Used)

A hardware-efficient approximation of LRU commonly used in set-associative caches.

---

### SHiP (Signature-based Hit Predictor)

A predictor-based cache replacement policy that uses program signatures to improve victim selection.

---

### Hawkeye

A predictor-based cache replacement policy inspired by Belady's optimal replacement algorithm.

---

## References

Each policy directory contains references to the original publications and additional documentation.

---

## License

MIT License