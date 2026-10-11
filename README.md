# Qiskit Fall Fest 2026 — Quantum Optimization O1: Max-Cut

**Status: four-graph architecture-aware QAOA simulation completed; 5-qubit Processor A and 9-node Processor B reconstructed from the supplied diagrams. Native gate set and synthetic noise parameters are participant-defined assumptions.**

This is a generalized, single-entry-point QAOA Max-Cut pipeline. It reads JSON graphs, computes exact classical Max-Cut baselines, optimizes QAOA with noiseless statevector expectation, transpiles the same logical circuit for two diagram-derived architectures with documented assumptions, runs ideal and synthetic-noise simulations, and exports trial-level CSV data, architecture metrics, plots and reports.

**Start with [report.md](report.md) for the updated nine-node four-graph findings.** See [TOPOLOGY_9Q_README.md](TOPOLOGY_9Q_README.md) for topology reconstruction and [OFFICIAL_REQUIREMENTS_PENDING.md](OFFICIAL_REQUIREMENTS_PENDING.md) for remaining assumptions.

## Contents

```text
main.py
src/{graphs,quantum,processors,validation,visualization}.py
processors/{processor_A,processor_B}.json
data/{graph1,graph2,graph3,graph4}.json
results/graph1/ ... results/graph4/
report.md
requirements.txt
OFFICIAL_REQUIREMENTS_PENDING.md
TOPOLOGY_9Q_README.md
EXISTING_RESULTS_PRESERVED.md
```

Each `results/graphN/` folder includes `trials.csv`, `summary.csv`, `paired_comparison.csv`, `architecture.csv`, `metadata.json`, `report.md`, compiled circuit dumps and PNG figures.

## Windows PowerShell / VS Code installation

Open the **repository root** in VS Code, then:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -c "import sys, qiskit, pandas, tabulate; print(sys.executable); print(qiskit.__version__)"
```

Ensure the Python path printed begins with this repository's `.venv` and not the old `O1_MaxCut` project's environment. `.venv` is excluded from Git.

## Reproduce the reported four-graph experiment

```powershell
python main.py --all --shots 4096 --trials 20 --restarts 3 --maxiter 100 --seed 42
```

Single-graph smoke test:

```powershell
python main.py --graph data/graph1.json --shots 256 --trials 2 --restarts 1 --maxiter 30
```

**Caution:** the short smoke test overwrites the outputs in `results/graph1`. To retain the final full-run outputs, back up `results/` first or rerun the full command above afterwards.

Run a new supported instance:

```powershell
python main.py --graph data/my_graph.json --shots 4096 --trials 20 --restarts 3 --maxiter 100
```

`--all` processes every `data/*.json` file, so adding new JSON files changes the batch size. Output folders are based on the JSON `name` field: use unique, safe names to avoid overwriting existing output directories.

## Input format

```json
{
  "name": "my_graph",
  "num_nodes": 5,
  "edges": [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]]
}
```

Positive weighted edges `[u,v,weight]` are supported. Vertices must be consecutively numbered starting at zero. Duplicate edges, loops and nonpositive weights are rejected. For these diagram-derived processors, at most five logical graph vertices fit both targets and permit a direct A/B comparison. The classical enumerator has a separate default safety limit of 18 nodes.

## What the outputs mean

- **Exact optimum:** the largest cut found by exhaustive classical enumeration.
- **Ideal QAOA expectation:** exact noiseless statevector expectation of the optimized p-layer ansatz.
- **Mean cut:** mean score across sampled measurement outcomes; not the maximum observed cut.
- **Approximation ratio:** sample mean cut divided by the exact optimum.
- **Paired B−A comparison:** the mean of trial-level differences indexed by matching seed; approximate 95% shot-sampling intervals, **not** hardware or reoptimization uncertainties.
- **Depth/CX excess:** relative to a fully connected *transpiled reference* with the same gate basis and optimization level; not an exact count of routing SWAPs.

Processor A is a 5-qubit reconstruction of the provided diagram; Processor B uses **all nine visible nodes** and 12 reconstructed connections from its diagram (whose printed label says seven qubits). The topology reconstructions, and particularly the edge interpretation and qubit numbering, are documented in `TOPOLOGY_9Q_README.md`. Configs retain `official: false` because gate basis, bidirectional CX and synthetic noise remain participant assumptions. The code explicitly accepts only configs labeled illustrative; do not change that flag casually.

## Submission and scientific limitations

- The three supplied documents show the A/B architecture diagrams but do not provide a unique machine-readable nine-node coupling map, calibration rates, or an O1 benchmark graph. The study therefore uses transparent diagram reconstruction and selected benchmark instances. **Do not claim a hardware-calibrated or uniquely specified official processor benchmark.**
- In updated nine-node experiments, B has lower compiled depth on all four graphs. Noisy trial-level B−A confidence intervals exclude zero for G1, G2 and G4; G3 is inconclusive. These findings are specific to the fixed layout and noise assumptions.
- Confidence intervals reflect fixed-parameter finite-shot sampling. Shared numeric seeds do not prove a strict common-random-number paired design. The four graph outcomes do not prove broad scalability or hardware performance.
- Verify the organizer's required repo name and format, official benchmark details, AI/LLM-use disclosure, repository accessibility, and clean-environment reproduction before submission.
- Generated results are committed as evidence; preserve full settings in `metadata.json` and trial CSV files. If rerunning with altered CLI options, clearly label/segregate the outputs.

## Final submission checklist

- [x] Exactly one problem statement: O1 Max-Cut
- [x] Generalized code and exact classical reference
- [x] Diagram-derived A/B compilation and ideal/noisy simulations
- [x] Four per-instance outputs and one consolidated report
- [x] Four-graph 5q/9q simulation results obtained
- [x] Clean-environment dependency installation and single-graph execution completed
- [x] Public GitHub repository access verified before this update
- [ ] Verify final 9q code/results/report have been pushed together
- [ ] Any additional organizer-mandated details and deadlines checked
- [ ] AI/LLM disclosure completed if required

**Acknowledgement:** AI assistance was used to help draft code and documentation; review the organizer's disclosure policy and include any mandated attribution or disclosure in the final submission.
