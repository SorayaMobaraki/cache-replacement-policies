# SHiP++ (Signature-Based Hit Predictor)

**SHiP++** is an enhanced version of the **Signature-Based Hit Predictor (SHiP)** cache replacement policy. It extends the original SHiP algorithm by improving cache insertion policies, Signature History Counter Table (SHCT) training, and prefetch-aware cache management to achieve higher cache performance while maintaining low hardware overhead.

SHiP++ was developed as a submission to the **Second Cache Replacement Championship (CRC-2)**, which evaluates state-of-the-art cache replacement policies using the ChampSim simulation framework. :contentReference[oaicite:1]{index=1}

---

## SHiP++ Architecture

<p align="center">
  <img src="Figures/SHiP_Context_Cache_Replacement.pdf" width="750">
</p>

<p align="center">
<em>Overview of the SHiP cache replacement policy. Figure adapted from my PhD thesis based on the original SHiP architecture.</em>
</p>

---

## Repository Structure

```text
SHiP/
├── README.md
├── Figures/
│   └── SHiP_Context_Cache_Replacement.pdf
├── ship++.cc
└── ship-hls/          # HLS implementation (Git submodule)
```

---

## C++ Implementation

This repository contains a C++ implementation of the **SHiP++** cache replacement policy.

The implementation incorporates the improvements proposed for CRC-2, including:

- Improved cache insertion policy
- Enhanced Signature History Counter Table (SHCT) training
- Writeback-aware insertion policy
- Prefetch-aware SHCT training
- Prefetch-aware cache insertion and promotion

These enhancements improve cache performance while preserving a low hardware overhead. :contentReference[oaicite:2]{index=2}

---

## HLS Implementation

The **ship-hls** submodule contains my High-Level Synthesis (HLS) implementation of the SHiP++ cache replacement policy.

The HLS implementation was developed as part of my research on FPGA-based hardware implementations of cache replacement policies and is maintained as an independent Git repository.

---

## Cache Replacement Championship (CRC-2)

SHiP++ was proposed as part of the **Second Cache Replacement Championship (CRC-2)**, an international competition that evaluates cache replacement algorithms using a common simulation framework and benchmark suite.

More information about the competition is available here:

https://crc2.ece.tamu.edu/?page_id=53 :contentReference[oaicite:3]{index=3}

---

## References

**SHiP**

C.-J. Wu, A. Jaleel, W. Hasenplaugh, M. Martonosi, S. C. Steely Jr., and J. Emer.

*SHiP: Signature-Based Hit Predictor for High Performance Caching.*

Proceedings of the 44th IEEE/ACM International Symposium on Microarchitecture (MICRO), 2011.

**SHiP++**

V. Young, C.-C. Chou, A. Jaleel, and M. Qureshi.

*SHiP++: Enhancing Signature-Based Hit Predictor for Improved Cache Performance.*

Second Cache Replacement Championship (CRC-2). :contentReference[oaicite:4]{index=4}

---

## Notes

- This repository provides a C++ implementation of the SHiP++ cache replacement policy.
- The `ship-hls` directory is maintained as a Git submodule containing the HLS implementation.
- The SHiP and SHiP++ algorithms were originally proposed by their respective authors.
- The HLS implementation was developed as part of my research on FPGA-based cache replacement policies.

---

## Author

**Soraya Mobaraki**

PhD in Computer Architecture  
University of Montpellier (LIRMM/CNRS)

GitHub: https://github.com/SorayaMobaraki