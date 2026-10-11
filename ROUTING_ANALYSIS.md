# Routing and SWAP Overhead — Phase 1 O1 Max-Cut

## Purpose and measurement definitions

This note interprets the recorded transpilation measurements for the **5-qubit Processor A** and **9-node Processor B** reconstructed from the provided diagrams. Both use the same assumed `rz`, `sx`, `x`, `cx` native gate basis, fixed initial placement, transpiler optimization level 1, and seed 42.

For each graph, the same QAOA circuit is compiled against:
- Each target processor's coupling map.
- An all-to-all coupling-map reference with the same gate basis and optimization level.

**Excess CX** = compiled target `cx_gates` − all-to-all reference `reference_cx`.

**Excess depth** = compiled target `depth` − all-to-all reference `reference_depth`.

These measurements show **connectivity-constrained compilation overhead**; they are *not* a count of inserted routing SWAPs. Compilation changes may also arise from mapping, synthesis, optimization and scheduling.

`explicit_swaps` counts `swap` instructions left **in the final native-basis circuit**. Since `swap` is absent from the allowed native gate set, a routing SWAP may have already been decomposed (commonly into CX operations). Consequently, **zero final explicit SWAP instructions must not be reported as zero routing SWAPs**.

## Recorded architecture metrics

| Graph | Target | Physical qubits | Depth | CX gates | Reference depth | Reference CX | Excess depth | Excess CX | Final explicit SWAP |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| G1 Original | A | 5 | 40 | 16 | 24 | 10 | 16 | 6 | 0 |
| G1 Original | B | 9 | 32 | 16 | 24 | 10 | 8 | 6 | 0 |
| G2 Cycle C5 | A | 5 | 35 | 19 | 24 | 10 | 11 | 9 | 0 |
| G2 Cycle C5 | B | 9 | 25 | 11 | 24 | 10 | 1 | 1 | 0 |
| G3 Star K1,4 | A | 5 | 29 | 11 | 21 | 8 | 8 | 3 | 0 |
| G3 Star K1,4 | B | 9 | 26 | 11 | 21 | 8 | 5 | 3 | 0 |
| G4 Complete K5 | A | 5 | 60 | 35 | 30 | 20 | 30 | 15 | 0 |
| G4 Complete K5 | B | 9 | 47 | 29 | 30 | 20 | 17 | 9 | 0 |

Values are transcribed from `results/graph1/architecture.csv` through `results/graph4/architecture.csv` produced with the updated B configuration.

## Interpretation

**Graph 1:** Both processors need 16 CX gates, but B is 8 circuit-depth layers shallower. Depth improvements need not imply fewer two-qubit operations.

**Graph 2:** B uses 11 CX gates versus A's 19, and depth 25 versus 35. Under the selected fixed qubit placement, the nine-node topology compiles this logical interaction pattern at substantially lower cost. It also gave the largest noisy mean-cut improvement in the separate simulation results.

**Graph 3:** Both use 11 CX gates; B is slightly shallower (26 versus 29). No statistically conclusive noisy mean-cut difference was observed.

**Graph 4:** B needs 29 CX versus A's 35, and depth 47 versus 60. The all-to-all reference is 20 CX and depth 30.

## What can and cannot be concluded

Supported:
- The architecture constrains transpilation and changes the native CX count and/or compiled depth for the fixed placement.
- The two target architectures produced different sampled mean-cut results under the chosen synthetic noise model.
- The reported *final native-circuit* SWAP instruction count is zero in all saved runs.

Not supported:
- “No routing SWAPs were inserted.” Native compilation may erase/decompose SWAP instructions.
- “Excess CX / 3 is the actual number of SWAP gates.” Compilation changes are not uniquely attributable to three-CX SWAP decomposition.
- Real hardware fidelity, calibrated performance or universal superiority of one topology.
- Separately attributable router-inserted SWAP count from the saved final circuit alone.

## Additional experiment if exact inserted-SWAP counts are required

To obtain a meaningful **pre-decomposition SWAP count**, add a separate instrumented routing-stage compilation or custom transpiler pass that records swap operations immediately *after routing and before gate-basis translation*. Keep its placement, routing method, seed and optimization settings explicit, and record the stage at which the number was measured. This is **not implemented by the current repository**, so its result must not be claimed.

## Reproducibility and limitations

The saved circuit dumps are `results/graphN/compiled_A.txt` and `compiled_B.txt`; the numerical architecture CSV files are the source of the table above. The circuit basis, bidirectional CX assumption, synthetic noise and nine-node diagram reconstruction are model choices described in `report.md` and `TOPOLOGY_9Q_README.md`. This analysis is not hardware calibration evidence.

The Phase-1 instructions mention routing/SWAP overhead; this repository provides native-circuit operation counts and a carefully labeled connectivity-overhead proxy, while **exact intermediate router-inserted SWAP counts remain unmeasured**.
