import stim
import pymatching
import matplotlib.pyplot as plt


def build_surface_code_circuit(distance=3, rounds=3):
    """
    Build a simple surface code circuit using stim's built-in generator.
    """
    circuit = stim.Circuit.generated(
        code_task="surface_code:rotated_memory_x",
        distance=distance,
        rounds=rounds,
        after_clifford_depolarization=0.001,
        after_reset_flip_probability=0.001,
        before_measure_flip_probability=0.001,
        before_round_data_depolarization=0.001,
    )
    return circuit


def export_surface_code_matching_graph(
    distance=3, rounds=3, output_svg="surface_code_matching_graph.svg"
):
    """
    Build a surface code circuit, extract its detector error model,
    create a pymatching.Matching object, and export the matching graph as an SVG.
    """
    print("=== Surface Code Matching Graph Demo ===")
    print(f"Building surface code circuit (distance={distance}, rounds={rounds}) ...")
    circuit = build_surface_code_circuit(distance=distance, rounds=rounds)
    print("Extracting detector error model ...")
    dem = circuit.detector_error_model(decompose_errors=True)
    print("Building pymatching.Matching object ...")
    matching = pymatching.Matching.from_detector_error_model(dem)
    print(f"Drawing matching graph to {output_svg} ...")
    fig, ax = plt.subplots(figsize=(6, 3))
    matching.draw()
    plt.savefig(output_svg)
    print(f"Matching graph SVG saved to {output_svg}")
    print(
        "You can open this SVG file to visualize the matching graph for the surface code circuit.\n"
    )
    return matching


if __name__ == "__main__":
    export_surface_code_matching_graph(
        distance=3, rounds=3, output_svg="surface_code_matching_graph.svg"
    )
