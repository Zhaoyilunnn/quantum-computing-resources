import matplotlib.pyplot as plt
from qiskit.visualization import plot_bloch_vector


plot_bloch_vector([0,1,0])
plt.savefig("bloch.png", dpi=300)
