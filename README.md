# Qiskit Fall Fest 2026 — Quantum Optimization O1: Max-Cut

**Status: four-graph illustrative architecture experiment completed; official benchmark requirements still unverified.**

This is a generalized, single-entry-point QAOA Max-Cut pipeline. It reads JSON graphs, computes exact classical Max-Cut baselines, optimizes QAOA with noiseless statevector expectation, transpiles the same logical circuit for two *illustrative* architectures, runs ideal and synthetic-noise simulations, and exports trial-level CSV data, architecture metrics, plots and reports.

**Start with [report.md](report.md) for the consolidated four-graph findings.** For unresolved rules, see [OFFICIAL_REQUIREMENTS_PENDING.md](OFFICIAL_REQUIREMENTS_PENDING.md).

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

Positive weighted edges `[u,v,weight]` are supported. Vertices must be consecutively numbered starting at zero. Duplicate edges, loops and nonpositive weights are rejected. For these *illustrative* processors, at most five logical graph vertices fit both targets and permit a direct A/B comparison. The classical enumerator has a separate default safety limit of 18 nodes.

## What the outputs mean

- **Exact optimum:** the largest cut found by exhaustive classical enumeration.
- **Ideal QAOA expectation:** exact noiseless statevector expectation of the optimized p-layer ansatz.
- **Mean cut:** mean score across sampled measurement outcomes; not the maximum observed cut.
- **Approximation ratio:** sample mean cut divided by the exact optimum.
- **Paired B−A comparison:** the mean of trial-level differences indexed by matching seed; approximate 95% shot-sampling intervals, **not** hardware or reoptimization uncertainties.
- **Depth/CX excess:** relative to a fully connected *transpiled reference* with the same gate basis and optimization level; not an exact count of routing SWAPs.

The processor configs are **participant-generated examples** (`official: false`), not official QFF A/B definitions. They use the same native gate set and illustrative depolarizing/readout noise rates. The scripts deliberately reject configs not explicitly marked illustrative; obtaining official specifications will require adapting and checking the backend configuration pathway, then **rerunning** the benchmark. Do not simply edit `official` to `true` and assume the pipeline is compatible.

## Submission and scientific limitations

- The supplied Phase-1 instructions require the exact organizer-defined O1 instance/constraints and A/B processor assumptions. These are not established by the provided PDFs. **Do not claim this repository has completed the official benchmark.**
- Four tested instances show that neither illustrative processor uniformly wins: B has an advantage on the cycle graph, A on the star graph, with inconclusive noisy quality differences on the other two graphs.
- Confidence intervals reflect fixed-parameter finite-shot sampling. Shared numeric seeds do not prove a strict common-random-number paired design. The four graph outcomes do not prove broad scalability or hardware performance.
- Verify the organizer's required repo name and format, official benchmark details, AI/LLM-use disclosure, repository accessibility, and clean-environment reproduction before submission.
- Generated results are committed as evidence; preserve full settings in `metadata.json` and trial CSV files. If rerunning with altered CLI options, clearly label/segregate the outputs.

## Final submission checklist

- [x] Exactly one problem statement: O1 Max-Cut
- [x] Generalized code and exact classical reference
- [x] Illustrative A/B compilation and ideal/noisy simulations
- [x] Four per-instance outputs and one consolidated report
- [ ] Organizer-defined O1 and official A/B inputs/configurations confirmed and run
- [ ] Fresh Python environment run completed and checked
- [ ] Repository naming, public/judge access, and final commit verified
- [ ] AI/LLM disclosure completed if required

**Acknowledgement:** AI assistance was used to help draft code and documentation; review the organizer's disclosure policy and include any mandated attribution or disclosure in the final submission.
