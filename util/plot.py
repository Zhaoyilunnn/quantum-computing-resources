from typing import Any, List, Optional, Tuple
import matplotlib.pyplot as plt


def plot_bar(data: List[Any],
             labels: List[Any],
             figsize: Optional[Tuple]=(8,6),
             figname: Optional[str]=None,
             rotation: Optional[int]=45,
             dpi: Optional[int]=300):
    """Plot a bar chart"""
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(1, 1, 1)
    ax.bar(range(len(data)), data)
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(labels, rotation=rotation)
    plt.tight_layout()
    plt.show()
    if figname:
        plt.savefig(figname, dpi=dpi)
