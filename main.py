import argparse
import json
from pathlib import Path

import pandas as pd
from qiskit import __version__ as qiskit_version

from src.graphs import load_graph, exact_baseline
from src.quantum import circuit, optimize_qaoa
from src.processors import (load_processors, compile_circuit,
                            circuit_metrics, reference_circuit)
from src.validation import run_validation
from src.visualization import plot_graph, plot_results

BASE = Path(__file__).resolve().parent


def experiment(path, args):
    graph = load_graph(path)
    configs = load_processors(BASE / 'processors')
    for label, config in configs.items():
        if graph['n'] > config['num_qubits']:
            raise ValueError(f"{graph['name']}: {graph['n']} vertices cannot fit Processor {label} ({config['num_qubits']} qubits). Use <=5 nodes for controlled A/B comparisons.")
    optimum, solutions = exact_baseline(graph)
    params, ideal_expectation = optimize_qaoa(graph, args.layers, args.restarts, args.seed, args.maxiter)
    logical = circuit(graph, params, args.layers)
    compiled = {label: compile_circuit(logical, config, args.seed) for label, config in configs.items()}
    metrics = []
    for label, qc in compiled.items():
        reference = reference_circuit(logical, configs[label], args.seed)
        observed = circuit_metrics(qc)
        baseline = circuit_metrics(reference)
        metrics.append({'processor': label, 'physical_qubits': configs[label]['num_qubits'],
                        **observed, 'reference_depth': baseline['depth'],
                        'reference_cx': baseline['cx_gates'],
                        'depth_overhead': observed['depth']-baseline['depth'],
                        'cx_overhead': observed['cx_gates']-baseline['cx_gates']})
    arch = pd.DataFrame(metrics)
    trials, summary, paired = run_validation(graph, optimum, compiled, configs,
                                             args.shots, args.trials, args.seed+1000)
    out = BASE / 'results' / graph['name']
    out.mkdir(parents=True, exist_ok=True)
    trials.to_csv(out/'trials.csv', index=False)
    summary.to_csv(out/'summary.csv', index=False)
    paired.to_csv(out/'paired_comparison.csv', index=False)
    arch.to_csv(out/'architecture.csv', index=False)
    for label, qc in compiled.items():
        (out/f'compiled_{label}.txt').write_text(str(qc.draw('text')),encoding='utf-8')
    plot_graph(graph, solutions[0], out/'maxcut_graph.png')
    plot_results(summary, arch, out)
    settings = {'graph':graph['name'],'nodes':graph['n'],'edges':graph['edges'],
                'exact_optimum':optimum,'optimal_partitions':len(solutions),
                'layers':args.layers,'optimized_parameters':params.tolist(),
                'ideal_uncompiled_expected_cut':ideal_expectation,'shots':args.shots,
                'trials':args.trials,'seed':args.seed,'restarts':args.restarts,
                'optimizer':'COBYLA with exact statevector expectation',
                'qiskit_version':qiskit_version,'processor_configs':'ILLUSTRATIVE',
                'noise':'1q depolarizing .001; CX depolarizing .02; readout .015',
                'limitations':'NOT an official organizer-defined benchmark'}
    (out/'metadata.json').write_text(json.dumps(settings,indent=2),encoding='utf-8')
    report = [f'# {graph["name"]} — O1 Max-Cut A/B experiment', '',
              '**Status: ILLUSTRATIVE ONLY; not an official organizer benchmark.**', '',
              f'- Graph: {graph["n"]} nodes; {len(graph["edges"])} edges',
              f'- Exact classical optimal cut: {optimum:g}',
              f'- p={args.layers}; statevector-optimized expected cut: {ideal_expectation:.6f}',
              f'- Shots per trial: {args.shots}; trial seeds: {args.trials}',
              '', '## A/B quality', '', summary.to_markdown(index=False), '',
              '## Architecture metrics', '', arch.to_markdown(index=False), '',
              '## Paired A/B differences', '', paired.to_markdown(index=False), '',
              '## Interpretation and limitations', '',
              'The two implementations use the same logical graph, QAOA parameters, transpilation seed,',
              'native gate basis and nominal illustrative noise rates. Circuit resource differences reflect',
              'the chosen example topology and layout, not measured IBM quantum hardware.',
              'Explicit SWAP count can be zero even when routing gates are decomposed into CX.',
              'Extra CX gates relative to a fully connected compilation are not an exact SWAP count.',
              'Intervals are approximate finite-shot confidence intervals at fixed parameters.',
              'Do not infer a hardware speed advantage from simulator runtime.', '',
              '## Missing official challenge information', '',
              '- Official O1 graph/instance and constraints',
              '- Official A/B coupling maps, native gate sets and noise assumptions',
              '- Organizer-defined benchmark reporting fields and repository naming',
              '- AI-assistance disclosure policy confirmation', '']
    (out/'report.md').write_text('\n'.join(report),encoding='utf-8')
    print(f'\n{graph["name"]}: exact optimum {optimum:g}; ideal QAOA expectation {ideal_expectation:.4f}')
    print(summary[['processor','mode','mean_cut','ci95_low','ci95_high']].to_string(index=False))
    print(arch[['processor','depth','cx_gates','depth_overhead','cx_overhead']].to_string(index=False))
    print('Saved to',out)


def main():
    parser = argparse.ArgumentParser(description='Generalized illustrative O1 Max-Cut pipeline')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--graph', help='Path to a graph JSON file')
    group.add_argument('--all', action='store_true', help='Run all data/*.json graphs')
    parser.add_argument('--layers', type=int, default=1)
    parser.add_argument('--restarts', type=int, default=4)
    parser.add_argument('--maxiter', type=int, default=150)
    parser.add_argument('--shots', type=int, default=4096)
    parser.add_argument('--trials', type=int, default=20)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    if min(args.layers,args.restarts,args.maxiter,args.shots,args.trials) < 1:
        parser.error('layers/restarts/maxiter/shots/trials must be positive')
    paths = sorted((BASE/'data').glob('*.json')) if args.all else [Path(args.graph)]
    if not paths:
        parser.error('No graph JSON files found')
    for path in paths:
        experiment(path, args)

if __name__ == '__main__':
    main()
