import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx


def plot_graph(graph, solution, path):
    g = nx.Graph()
    g.add_nodes_from(range(graph['n']))
    g.add_weighted_edges_from(graph['edges'])
    colors = ['skyblue' if bit == 0 else 'orange' for bit in solution]
    fig, ax = plt.subplots(figsize=(6, 5))
    nx.draw_networkx(g, pos=nx.spring_layout(g, seed=42), node_color=colors,
                     with_labels=True, node_size=850, ax=ax)
    ax.set_title(f"{graph['name']}: classical optimal partition")
    ax.axis('off')
    fig.tight_layout()
    fig.savefig(path, dpi=170)
    plt.close(fig)


def plot_results(summary, arch, out):
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(2)
    for offset, mode in [(-0.18, 'Ideal'), (0.18, 'Noisy')]:
        d = summary[summary['mode'] == mode].set_index('processor').loc[['A','B']]
        err = (d.ci95_high - d.mean_cut).to_numpy()
        ax.bar(x+offset, d.mean_cut, width=0.35, yerr=err, capsize=4, label=mode)
    ax.set_xticks(x, ['A', 'B'])
    ax.set_ylabel('Average Max-Cut')
    ax.set_title('Illustrative A/B mean cut (95% CI)')
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / 'cut_comparison.png', dpi=170)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    a = arch.set_index('processor').loc[['A','B']]
    ax.bar(x-0.18, a.depth, 0.35, label='Circuit depth')
    ax.bar(x+0.18, a.cx_gates, 0.35, label='CX gates')
    ax.set_xticks(x, ['A','B'])
    ax.set_title('Illustrative A/B circuit resources')
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / 'architecture.png', dpi=170)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x-0.18, a.depth_overhead, 0.35, label='Extra depth')
    ax.bar(x+0.18, a.cx_overhead, 0.35, label='Extra CX')
    ax.axhline(0, linewidth=1)
    ax.set_xticks(x, ['A','B'])
    ax.set_title('Compilation overhead vs fully connected reference')
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / 'compilation_overhead.png', dpi=170)
    plt.close(fig)
