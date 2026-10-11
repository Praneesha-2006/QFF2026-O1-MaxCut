# graph3 — O1 Max-Cut A/B experiment

**Status: ILLUSTRATIVE ONLY; not an official organizer benchmark.**

- Graph: 5 nodes; 4 edges
- Exact classical optimal cut: 4
- p=1; statevector-optimized expected cut: 3.000000
- Shots per trial: 4096; trial seeds: 20

## A/B quality

| processor   | mode   |   trials |   mean_cut |    sd_cut |   ci95_low |   ci95_high |   mean_approximation_ratio |   mean_optimal_probability |   mean_best_sampled_cut |
|:------------|:-------|---------:|-----------:|----------:|-----------:|------------:|---------------------------:|---------------------------:|------------------------:|
| A           | Ideal  |       20 |    3.00039 | 0.0151096 |    2.99377 |     3.00701 |                   0.750098 |                   0.451257 |                       4 |
| A           | Noisy  |       20 |    2.81967 | 0.0198202 |    2.81098 |     2.82835 |                   0.704916 |                   0.370337 |                       4 |
| B           | Ideal  |       20 |    3.00114 | 0.0202174 |    2.99227 |     3.01    |                   0.750284 |                   0.452588 |                       4 |
| B           | Noisy  |       20 |    2.77738 | 0.0224344 |    2.76755 |     2.78721 |                   0.694345 |                   0.347949 |                       4 |

## Architecture metrics

| processor   |   physical_qubits |   depth |   cx_gates |   two_qubit_gates |   explicit_swaps |   circuit_width |   reference_depth |   reference_cx |   depth_overhead |   cx_overhead |
|:------------|------------------:|--------:|-----------:|------------------:|-----------------:|----------------:|------------------:|---------------:|-----------------:|--------------:|
| A           |                 5 |      29 |         11 |                11 |                0 |               5 |                21 |              8 |                8 |             3 |
| B           |                 7 |      40 |         17 |                17 |                0 |               7 |                21 |              8 |               19 |             9 |

## Paired A/B differences

| mode   |   difference_B_minus_A |    ci95_low |   ci95_high |
|:-------|-----------------------:|------------:|------------:|
| Ideal  |            0.000744629 | -0.00479606 |  0.00628531 |
| Noisy  |           -0.0422852   | -0.0475096  | -0.0370607  |

## Interpretation and limitations

The two implementations use the same logical graph, QAOA parameters, transpilation seed,
native gate basis and nominal illustrative noise rates. Circuit resource differences reflect
the chosen example topology and layout, not measured IBM quantum hardware.
Explicit SWAP count can be zero even when routing gates are decomposed into CX.
Extra CX gates relative to a fully connected compilation are not an exact SWAP count.
Intervals are approximate finite-shot confidence intervals at fixed parameters.
Do not infer a hardware speed advantage from simulator runtime.

## Missing official challenge information

- Official O1 graph/instance and constraints
- Official A/B coupling maps, native gate sets and noise assumptions
- Organizer-defined benchmark reporting fields and repository naming
- AI-assistance disclosure policy confirmation
