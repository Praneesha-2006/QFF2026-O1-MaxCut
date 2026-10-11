# Processor B: nine-node diagram correction

## Why this update?
The official slide labels Processor B **7 qubits**, but the green network image has **9 distinct circles**. This benchmark implements the **pictured nine-node graph**. The differing printed label is documented as a discrepancy in the supplied slide.

This correction replaces only `processors/processor_B.json`. **Do not replace Processor A**: its five-node topology already matches the official slide.

## Node numbering assigned for reproducible compilation

| Qubit ID | Location in organizer's screenshot |
|---|---|
| 0 | Left |
| 1 | Upper-left |
| 2 | Lower-left |
| 3 | Center |
| 4 | Upper-middle |
| 5 | Lower-right-middle |
| 6 | Upper-right |
| 7 | Right |
| 8 | Bottom (pendant below center) |

## Undirected connections (12)

```
0-1  0-2
1-3  1-4
2-3
3-4  3-5  3-8
4-5  4-6
5-7
6-7
```

These edges were manually traced from the supplied nine-node screenshot. The edge list is a reconstruction of the drawn connections rather than a separate machine-readable specification. If better source information becomes available, revise the configuration and rerun.

The code's `src/processors.py` automatically expands each pair into bidirectional CX coupling directions, with `initial_layout=[0,1,2,3,4]` for five-node inputs. Hence the input numbering/placement is consequential and explicitly fixed.

## What is and is not confirmed

**Benchmark interpretation:** use the nine visible nodes in the supplied Processor B topology diagram and perform simulations with Qiskit Aer.

**Still participant assumptions:** the native gates (`rz`, `sx`, `x`, `cx`), directed-edge symmetry, compilation settings, and synthetic gate/readout noise rates. Preserve these caveats in the report. The JSON keeps `official: false` because these settings are not a complete organizer-provided backend calibration.

## Restore and rerun

1. Back up your old `results/` folder **outside** your project folder.
2. Copy `processors/processor_B.json` to the matching project destination, replacing the old file.
3. Run a short validation:

```
python main.py --graph data/graph2.json --shots 256 --trials 2 --restarts 1 --maxiter 30
```

4. If it passes, rerun all:

```
python main.py --all --shots 4096 --trials 20 --restarts 3 --maxiter 100 --seed 42
```

This overwrites all four results folders and changes A/B circuit metrics and statistics. **Do not keep the old consolidated `report.md` as the new benchmark report.** Update that document from the new result CSV files. The old GitHub reports remain as historical evidence until the new commit is pushed.

For a separate archive: `git tag pre-9q-processor-b` before updating your files.
