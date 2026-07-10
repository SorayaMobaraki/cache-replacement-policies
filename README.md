# Cache Replacement Policies

A collection of reference implementations, hardware prototypes, and documentation for modern cache replacement policies.

This repository provides software and hardware implementations of several cache replacement algorithms together with supporting documentation, validation frameworks, and experimental code. It is intended for students, researchers, and computer architects interested in cache memory systems, processor microarchitecture, and FPGA-based architectural exploration.

---

## Implemented Policies

This repository currently includes:

- **Least Recently Used (LRU)**
- **Pseudo Least Recently Used (PLRU)**
- **Signature-based Hit Predictor (SHiP)**
- **Hawkeye**

Depending on the replacement policy, implementations are available in:

- Python
- C++
- High-Level Synthesis (HLS)

---

## Repository Structure

```text
cache-replacement-policies/

├── LRU-PLRU/
│   ├── Figures/
│   ├── Python/
│   └── README.md
│
├── SHiP/
│   ├── ship-hls/
│   ├── Figures/
│   └── README.md
│
├── Hawkeye/
│   ├── Python/
│   ├── Cpp/
│   ├── hawkeye-hls/
│   ├── Figures/
│   └── README.md
│
└── README.md
```

---

## Objectives

- Provide reference implementations of classical and modern cache replacement policies.
- Document the design principles and hardware implementation of each algorithm.
- Support functional validation and algorithm comparison.
- Provide educational material for studying cache memory systems.
- Support FPGA- and HLS-based architectural research.

---

## Implemented Policies

### Least Recently Used (LRU)

A stack-based replacement policy that always evicts the cache block that has not been accessed for the longest period of time.

---

### Pseudo Least Recently Used (PLRU)

A hardware-efficient approximation of LRU that significantly reduces implementation complexity while maintaining comparable performance.

---

### Signature-based Hit Predictor (SHiP)

A predictor-based cache replacement policy that uses program signatures to predict future cache reuse and improve victim selection.

---

### Hawkeye

A predictor-based cache replacement policy inspired by Belady's optimal replacement algorithm. Hawkeye reconstructs optimal replacement decisions for sampled cache sets and uses this information to guide future cache replacement.

---

## References

Each policy directory contains:

- Background information
- Algorithm description
- Original research papers
- Implementation notes
- Validation methodology (where applicable)

---

## License

This project is released under the MIT License.

---

## Author

**Soraya Mobaraki**

PhD in Computer Architecture  
University of Montpellier (LIRMM/CNRS)

GitHub: https://github.com/SorayaMobaraki

LinkedIn: *(add your LinkedIn profile URL)*