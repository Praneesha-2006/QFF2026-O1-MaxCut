# Qiskit Fall Fest 2026 — Phase 1 O1 Max-Cut
## Consolidated four-graph architecture study

**Benchmark status: ILLUSTRATIVE / PRELIMINARY — NOT THE OFFICIAL ORGANIZER BENCHMARK.**

**Problem statement:** Quantum Optimization O1 — Max-Cut.  
**Method:** QAOA with one cost/mixer layer (p=1), COBYLA optimization of the *ideal exact-statevector* mean-cut objective (three starts; 100 maximum COBYLA iterations per start), exact brute-force classical baseline, and two illustrative architecture-dependent transpilation targets.  
**Simulation:** Qiskit Aer ideal and synthetic-noise simulations; 20 runs with 4,096 shots per processor × noise condition × graph. Seed 42 for optimization/transpilation; trial seeds 1042–1061.  
**Scope:** four unweighted graphs of 4–5 vertices, each fitting on both illustrative A/B processors.

## 1. Setup and benchmarks

- Graph 1 — original four-vertex, five-edge graph; exact optimum 4.
- Graph 2 — five-cycle C5; exact optimum 4.
- Graph 3 — five-vertex star K1,4; exact optimum 4.
- Graph 4 — complete five-vertex graph K5; exact optimum 6.

The classical reference enumerates all 2^n bit assignments and returns the maximum cut. The quantum result is evaluated as the *mean measured cut* (plus best sampled cut, optimal-solution probability and mean approximation ratio). A sampled maximum and a mean-cut score are distinct metrics. Input graphs may also have positive finite edge weights.

## 2. Illustrative processor definitions

| Parameter | Processor A | Processor B |
|---|---|---|
| Physical qubits | 5 | 7 |
| Undirected coupling edges | (0,1), (0,2), (0,3), (3,4) | (0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,0), (2,6) |
| Native basis | rz, sx, x, cx | rz, sx, x, cx |
| Layout | Initial logical qubits 0…n−1 | Same |
| Synthetic noise | Identical rates | Identical rates |

Noise: single-qubit depolarization probability 0.001 on `sx` and `x`, CX depolarization 0.02, and symmetric readout bit-flip rate 0.015. A and B share these illustrative nominal rates, so these experiments emphasize the selected connectivity and compiled circuits; actual hardware error rates are not measured. See `processors/*.json` and `src/processors.py` for exact implementation.

## 3. Classical and ideal-QAOA references

| Graph | Nodes | Edges | Exact Max-Cut | Ideal p=1 QAOA expectation | Ideal expectation / optimum |
|---|---:|---:|---:|---:|---:|
| G1 — Original | 4 | 5 | 4 | 3.237109 | 0.8093 |
| G2 — Cycle C5 | 5 | 5 | 4 | 3.750000 | 0.9375 |
| G3 — Star K1,4 | 5 | 4 | 4 | 3.000000 | 0.7500 |
| G4 — Complete K5 | 5 | 10 | 6 | 5.905212 | 0.9842 |

The ideal expected value represents the particular optimized p=1 QAOA ansatz, **not** the exact classical maximum. In particular, the star graph's expected value of 3 does not indicate that the exact optimum was calculated incorrectly. We have not established global optimality of the variational parameters.

## 4. Measured mean-cut performance

| Graph | A ideal | B ideal | A noisy | B noisy | Noisy B−A |
|---|---:|---:|---:|---:|---:|
| G1 | 3.232336 | 3.239844 | 3.060974 | 3.064758 | +0.003784 |
| G2 | 3.749219 | 3.746851 | 3.458057 | 3.520776 | +0.062720 |
| G3 | 3.000391 | 3.001135 | 2.819666 | 2.777380 | −0.042285 |
| G4 | 5.902002 | 5.902002 | 5.615796 | 5.614648 | −0.001147 |

These are means of 20 trial-level sample means (4,096 shots each). See `results/graph*/summary.csv` for mean-cut confidence bounds, optimal-solution frequency and approximation ratios.

## 5. Paired A/B statistical comparison

**Difference is B minus A.** Confidence limits are the code's approximate `mean ± 1.96 × sample standard error` intervals over 20 trials, evaluated at *fixed optimized parameters and one synthetic noise model*. They are **not** end-to-end uncertainty estimates accounting for reoptimization, varying calibration, hardware, or between-graph generalization.

| Graph | Ideal B−A (95% CI) | Noisy B−A (95% CI) | Noisy inference under simulation model |
|---|---|---|---|
| G1 | +0.007507 [0.002184, 0.012831] | +0.003784 [−0.001046, 0.008614] | Inconclusive |
| G2 | −0.002368 [−0.005982, 0.001246] | +0.062720 [0.056623, 0.068816] | B better |
| G3 | +0.000745 [−0.004796, 0.006285] | −0.042285 [−0.047510, −0.037061] | A better |
| G4 | 0.000000 [0, 0] | −0.001147 [−0.004105, 0.001810] | Inconclusive |

**Important interpretation:** The small nonzero G1 *ideal* difference is sampling variation; both architectures should theoretically implement the same logical ideal QAOA state, subject to correct compilation and measurement mapping. The identical G4 ideal samples arise from these simulations/seeds, not hardware equivalence. Matching integer seeds across differently compiled circuits is not by itself a guarantee of statistically paired random noise; the program labels trials by shared seed, and the reported intervals should be read as descriptive finite-shot estimates rather than a fully justified common-random-number experimental design. The graph-specific findings were not corrected for multiple hypothesis testing.

## 6. Compilation and architectural resource metrics

| Graph | A depth | B depth | A CX | B CX | A excess depth | B excess depth | A excess CX | B excess CX |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| G1 | 40 | 35 | 16 | 16 | 16 | 11 | 6 | 6 |
| G2 | 35 | 27 | 19 | 16 | 11 | 3 | 9 | 6 |
| G3 | 29 | 40 | 11 | 17 | 8 | 19 | 3 | 9 |
| G4 | 60 | 58 | 35 | 38 | 30 | 28 | 15 | 18 |

The reference is the *same transpiler settings with an all-to-all coupling map*, not an uncompiled circuit. Depth and CX excess are proxy measures for connectivity/compilation overhead, **not exact SWAP counts**. In this native basis, routing operations can be decomposed to CX, so every compiled circuit reports zero *explicit* `swap` instructions despite overhead. No runtime or hardware resource advantage is claimed.

- **Cycle (G2):** B's compilation reduces depth by 8 and CX by 3; its noisy mean cut is higher by 0.062720.
- **Star (G3):** A's compilation reduces depth by 11 and CX by 6; its noisy mean cut is higher by 0.042285.
- **Complete graph (G4):** B is 2 layers shallower but uses 3 **more** CX operations; noisy quality is inconclusive.
- **Original graph (G1):** B is 5 layers shallower with equal CX; noisy quality is inconclusive.

These results are consistent with the impact of graph interaction patterns and physical connectivity on compiled quantum circuits. They do **not** establish connectivity as the sole cause of observed differences or show that either processor is universally superior.

## 7. Reproducibility

From the repository root in a fresh Python 3.13 environment:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -c "import sys; print(sys.executable)"
python main.py --all --shots 4096 --trials 20 --restarts 3 --maxiter 100 --seed 42
```

Per-graph outputs are written to `results/graph1` through `results/graph4`. Check `metadata.json` for optimizer settings, Qiskit version, parameter values, shot counts and seeds; `trials.csv` contains trial-level evidence and `paired_comparison.csv` contains paired-difference summaries. Baseline reproduction may depend on operating-system package resolution and simulator details. The clean-environment reproduction has **not** been independently verified as part of this static audit.

## 8. Submission status and limitations

1. **Official specifications unverified:** organizer-approved O1 input instance(s), exact Processor A/B topology, basis, noise assumptions, metrics and any template rules are not established by the supplied starter guidance. Thus none of the numeric findings can be described as the official Phase-1 A/B benchmark.
2. **Synthetic simulator, not quantum hardware:** no device calibration, gate duration, real-hardware noise, queue time or platform run cost was measured.
3. **Algorithm scope:** shallow p=1 QAOA, 4–5 node example set, exact ideal parameter optimization, positive-weight Max-Cut. Scaling to larger graph sizes is limited by the illustrative 5-qubit A and 7-qubit B targets; a controlled comparison is limited to at most five logical vertices.
4. **Statistical scope:** repeated shot sampling at fixed parameters, 20 trial seeds, approximate normal intervals; no optimizer uncertainty or robustness sweeps.
5. **Reproducibility and disclosure:** verify fresh installation, judge access, official repository naming and required AI-assistance disclosure before submission. The root README and `OFFICIAL_REQUIREMENTS_PENDING.md` document the outstanding items.

**Phase 1 is the A/B comparison. Processor C/D and the Bell architecture task are Phase 2 per the participant instructions.**

## 9. Output index

- `results/graph1/` through `results/graph4/` — full per-graph numerical evidence and figures.
- `results/graph*/report.md` — automatically generated per-graph analyses.
- `results/graph*/metadata.json` — parameters, seeds, baseline and noise description.
- `EXISTING_RESULTS_PRESERVED.md` — context on development-era results.
- `OFFICIAL_REQUIREMENTS_PENDING.md` — mandatory organizer confirmation checklist.
