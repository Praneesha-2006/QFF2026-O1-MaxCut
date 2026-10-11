# graph2 — O1 Max-Cut A/B experiment

**Status: ILLUSTRATIVE ONLY; not an official organizer benchmark.**

- Graph: 5 nodes; 5 edges
- Exact classical optimal cut: 4
- p=1; statevector-optimized expected cut: 3.750000
- Shots per trial: 4096; trial seeds: 20

## A/B quality

| processor   | mode   |   trials |   mean_cut |     sd_cut |   ci95_low |   ci95_high |   mean_approximation_ratio |   mean_optimal_probability |   mean_best_sampled_cut |
|:------------|:-------|---------:|-----------:|-----------:|-----------:|------------:|---------------------------:|---------------------------:|------------------------:|
| A           | Ideal  |       20 |    3.74922 | 0.0112438  |    3.74429 |     3.75415 |                   0.937305 |                   0.878906 |                       4 |
| A           | Noisy  |       20 |    3.45806 | 0.0135972  |    3.4521  |     3.46402 |                   0.864514 |                   0.736792 |                       4 |
| B           | Ideal  |       20 |    3.74685 | 0.00955845 |    3.74266 |     3.75104 |                   0.936713 |                   0.877722 |                       4 |
| B           | Noisy  |       20 |    3.52078 | 0.0118693  |    3.51557 |     3.52598 |                   0.880194 |                   0.765942 |                       4 |

## Architecture metrics

| processor   |   physical_qubits |   depth |   cx_gates |   two_qubit_gates |   explicit_swaps |   circuit_width |   reference_depth |   reference_cx |   depth_overhead |   cx_overhead |
|:------------|------------------:|--------:|-----------:|------------------:|-----------------:|----------------:|------------------:|---------------:|-----------------:|--------------:|
| A           |                 5 |      35 |         19 |                19 |                0 |               5 |                24 |             10 |               11 |             9 |
| B           |                 7 |      27 |         16 |                16 |                0 |               7 |                24 |             10 |                3 |             6 |

## Paired A/B differences

| mode   |   difference_B_minus_A |    ci95_low |   ci95_high |
|:-------|-----------------------:|------------:|------------:|
| Ideal  |            -0.00236816 | -0.00598206 |  0.00124573 |
| Noisy  |             0.0627197  |  0.0566231  |  0.0688164  |

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
