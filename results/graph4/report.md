# graph4 — O1 Max-Cut A/B experiment

**Status: ILLUSTRATIVE ONLY; not an official organizer benchmark.**

- Graph: 5 nodes; 10 edges
- Exact classical optimal cut: 6
- p=1; statevector-optimized expected cut: 5.905212
- Shots per trial: 4096; trial seeds: 20

## A/B quality

| processor   | mode   |   trials |   mean_cut |    sd_cut |   ci95_low |   ci95_high |   mean_approximation_ratio |   mean_optimal_probability |   mean_best_sampled_cut |
|:------------|:-------|---------:|-----------:|----------:|-----------:|------------:|---------------------------:|---------------------------:|------------------------:|
| A           | Ideal  |       20 |     5.902  | 0.0070137 |    5.89893 |     5.90508 |                   0.983667 |                   0.975488 |                       6 |
| A           | Noisy  |       20 |     5.6158 | 0.0105409 |    5.61118 |     5.62042 |                   0.935966 |                   0.842664 |                       6 |
| B           | Ideal  |       20 |     5.902  | 0.0070137 |    5.89893 |     5.90508 |                   0.983667 |                   0.975488 |                       6 |
| B           | Noisy  |       20 |     5.6467 | 0.0102134 |    5.64223 |     5.65118 |                   0.941117 |                   0.856262 |                       6 |

## Architecture metrics

| processor   |   physical_qubits |   depth |   cx_gates |   two_qubit_gates |   explicit_swaps |   circuit_width |   reference_depth |   reference_cx |   depth_overhead |   cx_overhead |
|:------------|------------------:|--------:|-----------:|------------------:|-----------------:|----------------:|------------------:|---------------:|-----------------:|--------------:|
| A           |                 5 |      60 |         35 |                35 |                0 |               5 |                30 |             20 |               30 |            15 |
| B           |                 9 |      47 |         29 |                29 |                0 |               9 |                30 |             20 |               17 |             9 |

## Paired A/B differences

| mode   |   difference_B_minus_A |   ci95_low |   ci95_high |
|:-------|-----------------------:|-----------:|------------:|
| Ideal  |              0         |  0         |   0         |
| Noisy  |              0.0309082 |  0.0256037 |   0.0362127 |

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
