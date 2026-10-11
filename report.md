# Qiskit Fall Fest 2026 — Phase 1 O1 Max-Cut
## Consolidated four-graph architecture-aware results (5-qubit A / 9-node B)

**Experiment scope:** Qiskit Aer simulation using two processor coupling graphs reconstructed from the supplied challenge diagrams. Exact nine-node numbering, native-gate assumptions and synthetic noise are documented; the experiment does **not** claim device calibration or real-hardware execution.

## 1. Method

- One selected problem statement: Quantum Optimization O1 — Max-Cut.
- Graph JSON inputs: G1 original four-node graph; G2 cycle C5; G3 star K1,4; G4 complete K5.
- Exact classical baseline by enumeration of all bit assignments for each small graph.
- QAOA p=1, COBYLA optimization using exact noiseless statevector expectation; three starting points, 100 iteration limit, seed 42.
- Identical logical circuit/optimized angles for A and B on the same graph; native-basis transpilation with initial layout physical qubits `[0, 1, ..., n−1]`, optimization level 1, seed 42.
- Qiskit Aer: 20 trials, 4,096 shots per condition and graph; ideal and synthetic-noise conditions.

## 2. Processor assumptions

| Parameter | Processor A | Processor B |
|---|---|---|
| Graph size | 5 nodes | 9 nodes |
| Coupling edges | (0,1), (0,2), (0,3), (3,4) | (0,1), (0,2), (1,3), (1,4), (2,3), (3,4), (3,5), (3,8), (4,5), (4,6), (5,7), (6,7) |
| Two-qubit connectivity interpretation | Undirected pairs expanded into both CX directions | Same |
| Assumed basis | `rz`, `sx`, `x`, `cx` | Same |
| Assumed gate/noise rates | Same across A/B | Same across A/B |

The Processor B diagram is captioned as seven qubits but contains nine visible nodes. This study uses the nine-node graph shown in the diagram; its qubit numbering and traced edge interpretation are explained in `TOPOLOGY_9Q_README.md`. The diagram does not provide calibrated native gate rates. The code assumes one-qubit depolarizing probability 0.001 on `sx`/`x`, two-qubit depolarizing probability 0.02 on `cx`, and readout error probability 0.015 per bit, applied identically to both targets. These are **synthetic modeling choices**, not verified hardware calibrations.

## 3. Classical references and mean-cut results

| Graph | Nodes | Edges | Exact optimum | Ideal p=1 expectation | A ideal | B ideal | A noisy | B noisy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| G1 — Original | 4 | 5 | 4 | 3.237109 | 3.232336 | 3.239844 | 3.060974 | 3.075476 |
| G2 — Cycle C5 | 5 | 5 | 4 | 3.750000 | 3.749219 | 3.746436 | 3.458057 | 3.549219 |
| G3 — Star K1,4 | 5 | 4 | 4 | 3.000000 | 3.000391 | 3.002051 | 2.819666 | 2.824304 |
| G4 — Complete K5 | 5 | 10 | 6 | 5.905212 | 5.902002 | 5.902002 | 5.615796 | 5.646704 |

The classical optimum is the maximum possible cut; the reported QAOA mean cut is the average score of samples, not the largest sampled score. Ideal p=1 expectations can be below the classical optimum.

## 4. Trial-level A/B difference and uncertainty

The differences below are `B−A`. The intervals are approximate 95% trial-level intervals calculated as mean ± 1.96 × standard error across 20 trials under fixed parameters and the chosen synthetic noise model. They do not cover alternative topology reconstructions, optimizer initialization uncertainty, hardware calibrations or differences between graph families.

| Graph | Ideal B−A [95% CI] | Noisy B−A [95% CI] | Noisy conclusion |
|---|---|---|---|
| G1 — Original | +0.007507 [+0.002184, +0.012831] | +0.014502 [+0.009665, +0.019339] | B higher under modeled conditions |
| G2 — Cycle C5 | -0.002783 [-0.007092, +0.001526] | +0.091162 [+0.084499, +0.097825] | B higher under modeled conditions |
| G3 — Star K1,4 | +0.001660 [-0.002757, +0.006077] | +0.004639 [-0.001164, +0.010442] | Inconclusive |
| G4 — Complete K5 | +0.000000 [+0.000000, +0.000000] | +0.030908 [+0.025604, +0.036213] | B higher under modeled conditions |

For Graph 3 the noisy difference interval includes zero. Graphs 1, 2, and 4 show positive differences under the reported model; these exploratory comparisons are not adjusted for multiple testing. Identical ideal Graph 4 trial outcomes reflect deterministic simulation/seed behavior and do not prove physical equivalence. Matching simulator seeds does not guarantee independent physical noise realizations or rigorous common-random-number pairing.

## 5. Compiled architecture metrics

| Graph | A depth | B depth | A CX | B CX | A excess depth | B excess depth | A excess CX | B excess CX |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| G1 — Original | 40 | 32 | 16 | 16 | 16 | 8 | 6 | 6 |
| G2 — Cycle C5 | 35 | 25 | 19 | 11 | 11 | 1 | 9 | 1 |
| G3 — Star K1,4 | 29 | 26 | 11 | 11 | 8 | 5 | 3 | 3 |
| G4 — Complete K5 | 60 | 47 | 35 | 29 | 30 | 17 | 15 | 9 |

Processor B gives lower compiled depth for all four fixed-layout experiments; G2 and G4 also use fewer native CX operations. These results depend on the particular graph-to-physical-qubit placement and Qiskit transpiler settings. **A shallow circuit does not alone imply lower hardware error; the observed noisy quality is evaluated separately.**

### Routing-overhead interpretation

The `reference_circuit` function transpiles the same circuit against an all-to-all coupling graph, with the same native gate basis and transpiler settings. **Excess depth** = target depth minus reference depth; **excess CX** = target CX count minus reference CX count. These figures are compilation-overhead proxies, not exact SWAP insertion counts or exclusively routing costs. Gate decomposition, gate cancellation, and scheduling can also affect the difference. Because the final native gate basis excludes `swap`, a routing SWAP may be decomposed into CX gates; `explicit_swaps = 0` is not evidence that no routing occurred. This experiment does **not** claim a calibrated or separately attributed count of physical SWAP operations.

### Interpretation by graph

- **G1 Original:** B depth 32 versus A 40, but CX counts equal (16). B has a small positive noisy difference under the model; avoid assigning it exclusively to CX reduction.
- **G2 Cycle:** B depth 25 vs A 35 and CX 11 vs A 19. Largest observed positive noisy B−A difference (+0.091162).
- **G3 Star:** B depth 26 vs A 29, both with 11 CX. Noisy difference is inconclusive.
- **G4 Complete:** B depth 47 vs A 60 and CX 29 vs A 35. Positive noisy B−A difference (+0.030908).

## 6. Reproducibility

From the repository root after installing `requirements.txt`:

```powershell
python main.py --all --shots 4096 --trials 20 --restarts 3 --maxiter 100 --seed 42
```

The command overwrites `results/graph*/` and requires the corrected `processors/processor_B.json`. Each per-graph folder contains `summary.csv`, `trials.csv`, `paired_comparison.csv`, `architecture.csv`, `metadata.json`, transpiled circuit dumps, figures and an individual `report.md`. Ensure the entire four-graph results directory is regenerated before pushing to GitHub.

## 7. Scope and limitations

1. The processor network edges and qubit IDs are reconstructed from the diagram. The original slide uses a seven-qubit label next to a nine-node drawing; the nine-node interpretation is used here. The gate basis, noise rates and bidirectional CX permissions remain documented modeling assumptions.
2. The experiment tests four selected small Max-Cut instances, not all graph families or large-graph scaling. Fair A/B benchmarking is limited to the smaller five-qubit architecture’s capacity.
3. The experiment uses simulation, not real IBM hardware; no physical fidelity, calibration data or queue/run-time advantage was measured.
4. The statistical intervals describe fixed-parameter finite-shot variation only and are not corrected for multiple testing.
5. The output includes two-qubit CX/depth excess, **not** a directly identifiable SWAP count. The native-gate circuit can have zero explicit SWAP instructions after decomposition.
6. Check the submission portal, naming rules, and AI-assistance disclosure separately. The public repository is an implementation artifact, not proof of final submission.

**Conclusion:** For the reconstructed nine-node Processor B and documented synthetic noise model, B compiles the tested QAOA circuits to lower depth in all four graph instances, and shows higher noisy mean-cut estimates with trial-level intervals excluding zero on G1, G2 and G4. The star graph’s noisy difference is inconclusive. The conclusions are conditional on the selected placement, processor reconstruction, compilation settings and noise model.
