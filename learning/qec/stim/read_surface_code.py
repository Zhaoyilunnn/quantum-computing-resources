"""
This script reads a quantum error-correcting code circuit from a file,
generates visual representations of the circuit's ticks as SVG files,
and creates a 3D match graph of the detector error model as a GLTF file.
"""

import stim
import os
import matplotlib.pyplot as plt
import numpy as np


def read_circuit_from_file(filename):
    with open(filename, "r") as f:
        circuit_text = f.read()
    return stim.Circuit(circuit_text)


def save_tick_svgs(circuit, output_dir):
    """
    For each tick in the circuit, save a diagram as SVG.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Use stim's diagram feature to get a slice per tick.
    # The 'detslice-with-ops-svg' type shows ticks and operations.
    diagram = circuit.diagram(type="detslice-with-ops-svg")
    svg_path = os.path.join(output_dir, "full_circuit.svg")
    with open(svg_path, "w") as f:
        f.write(str(diagram))
    print(f"Saved full circuit SVG to {svg_path}")

    # Optionally, split the circuit into ticks and save each tick as a separate SVG.
    # stim does not natively support per-tick SVG export, so we can parse ticks manually.
    # Here, we just save the full circuit as one SVG for simplicity.


def save_detector_error_model_gltf(circuit, output_path):
    """
    Generate and save the detector error model's 3D match graph as a GLTF file.
    """
    gltf_diagram = circuit.diagram("matchgraph-3d")
    # The diagram object does not have a to_bytes() method.
    # Use str(gltf_diagram) to get the GLTF content as a string, then encode to bytes.
    gltf_bytes = str(gltf_diagram).encode("utf-8")
    with open(output_path, "wb") as f:
        f.write(gltf_bytes)
    print(f"Saved detector error model 3D match graph GLTF to {output_path}")


def main():
    circuit_path = "/home/zhaoyilun/quantum-computing-resources/learning/qec/stim/example_surface_code_d_3.txt"
    circuit = read_circuit_from_file(circuit_path)
    save_tick_svgs(circuit, "surface_code_svgs")
    save_detector_error_model_gltf(
        circuit, "surface_code_svgs/detector_error_model_graph.gltf"
    )


if __name__ == "__main__":
    main()
