from typing import Any, List, Optional, Tuple, Union
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def plot_bar(data: List[Any] | List[List[Any]],
             labels: List[Any],
             data_labels: Optional[List[Any]]=None,
             width: float=0.3,
             figsize: Optional[Tuple]=(8,6),
             figname: Optional[str]=None,
             rotation: Optional[int]=45,
             dpi: Optional[int]=300):
    """Plot a bar chart
    Args:
        data (List[Any] | List[List[Any]]): can be a list of bar values or
            multiple list of bar values
        labels (List[Any]): labels of x-axis
        data_labels (Optional[List[Any]]): labels of each group of bar data
        width: Width of each bar
        figsize: Size of the figure
        rotation: Rotation angle of x-axis labels
        dpi: Resolution of the figure
    """
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(1, 1, 1)
    # Set positions
    x = []
    if isinstance(data[0], list): # Plot multiple groups
        x = np.arange(len(data[0]))
        if data_labels is None:
            raise ValueError("Please set a label for each group of data.")
        num_groups = len(data)
        num_left = num_groups // 2
        start_pos = x - num_left*width
        for i in range(num_groups):
            ax.bar(start_pos+width*i, data[i], width, label=data_labels[i])
    else: # Plot single group
        x = np.arange(len(data))
        ax.bar(x, data)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=rotation)
    ax.legend()
    plt.tight_layout()
    plt.show()
    if figname:
        plt.savefig(figname, dpi=dpi)


def plot_bar_3d(
        data: List[Union[Any, Any, Any]],
        labels: Union[Any, Any, Any],
        data_labels: Optional[List[Any]]=None,
        width: float=0.3,
        figsize: Optional[Tuple]=(8,6),
        figname: Optional[str]=None,
        rotation: Optional[int]=45,
        dpi: Optional[int]=300
    ):
    """Plot a bar chart
    Args:
        data (List[Union[Any, Any, Any]]): List of (x_position, y_position, dz)
    """
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')

    xpos, ypos, dz = zip(*data)
    print(xpos)
    print(ypos)
    print(dz)
    cmap = ListedColormap(['r', 'g', 'b'])
    # Normalize the dz values to range from 0 to 2*pi
    norm = plt.Normalize(min(dz), max(dz))
    zpos = np.zeros(len(data))
    dx = np.ones(len(data))
    dy = np.ones(len(data))
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=cmap(norm(dz)))
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.set_zlabel(labels[2])

    plt.tight_layout()
    plt.show()
    if figname:
        plt.savefig(figname, dpi=dpi)
