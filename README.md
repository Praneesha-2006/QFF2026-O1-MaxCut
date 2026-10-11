# Qiskit Fall Fest 2026 — O1: Max-Cut

## Project Overview

This project implements the **Quantum Approximate Optimization Algorithm (QAOA)** for the Max-Cut problem and compares its performance across two processor connectivity models using **Qiskit Aer**. The study evaluates how hardware topology affects circuit compilation and solution quality under ideal and simulated noisy conditions.

## Approach

- **Problem:** Quantum Optimization (O1) — Max-Cut.
- **Algorithm:** QAOA with one layer (`p=1`), optimized using COBYLA.
- **Classical baseline:** Exact Max-Cut solution by exhaustive search.
- **Processor A:** Five-qubit connectivity graph.
- **Processor B:** Nine-node connectivity graph reconstructed from the provided diagram.
- **Evaluation:** Ideal/noisy mean cut, confidence intervals, circuit depth, CX gates, and connectivity-related compilation overhead.

Both architectures use the same logical QAOA circuit and the same assumed native gates (`rz`, `sx`, `x`, `cx`). Noise parameters are synthetic and applied consistently; these are **simulation models, not calibrated physical devices**.

## Setup and Execution

Use Python 3.13 and run the following commands from the repository root in Windows PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Reproduce all four benchmark experiments:

```powershell
python main.py --all --shots 4096 --trials 20 --restarts 3 --maxiter 100 --seed 42
```

The command regenerates files in `results/`.

To run a single graph:

```powershell
python main.py --graph data/graph2.json --shots 4096 --trials 20 --restarts 3 --maxiter 100 --seed 42
```

## Benchmark Results

Each processor was evaluated using **20 trials of 4,096 shots** per graph and simulation condition.

| Graph | Exact Max-Cut | A noisy mean cut | B noisy mean cut | A depth | B depth |
|---|---:|---:|---:|---:|---:|
| G1 — Original | 4 | 3.0610 | 3.0755 | 40 | 32 |
| G2 — Cycle C5 | 4 | 3.4581 | 3.5492 | 35 | 25 |
| G3 — Star K1,4 | 4 | 2.8197 | 2.8243 | 29 | 26 |
| G4 — Complete K5 | 6 | 5.6158 | 5.6467 | 60 | 47 |

**Observation:** Processor B produces lower compiled circuit depth on all four graphs. Its noisy mean-cut improvement is supported by the reported trial-level 95% intervals for G1, G2, and G4; the difference for G3 is inconclusive. Findings are specific to the selected architectures, layout, and synthetic noise model.

## Repository Structure

```text
main.py                        # Run experiments
src/                           # QAOA, processor, evaluation and plotting modules
data/                          # Four benchmark Max-Cut graphs
processors/                    # Processor A and B configurations
results/                       # Trial data, metrics, plots and per-graph reports
report.md                      # Full methodology and statistical analysis
ROUTING_ANALYSIS.md            # Circuit routing and overhead interpretation
TOPOLOGY_9Q_README.md          # Processor B reconstruction details
requirements.txt               # Python dependencies
```

## Results and Documentation

The `results/graph1` through `results/graph4` folders contain the generated CSV measurements, architecture metrics, compiled circuits and figures. Refer to [report.md](report.md) for detailed experimental findings, [ROUTING_ANALYSIS.md](ROUTING_ANALYSIS.md) for the limitations of SWAP measurement, and [TOPOLOGY_9Q_README.md](TOPOLOGY_9Q_README.md) for topology assumptions.

**Note:** The current routing metric is excess depth/CX relative to an all-to-all reference; it is **not** an exact pre-decomposition count of inserted SWAP operations. The nine-node Processor B graph is reconstructed from the pictured nodes; its native gates and noise rates are documented modeling assumptions.
