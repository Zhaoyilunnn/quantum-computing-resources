import stim
import pymatching
import numpy as np


def build_simple_repetition_code_circuit(distance=3, rounds=3):
    """
    Build a simple repetition code circuit using stim.
    This code protects against bit-flip (X) errors.
    """
    circuit = stim.Circuit()
    # Data qubits: 0, 2, 4; Measurement qubits: 1, 3
    n_data = distance
    n_meas = distance - 1

    # Initialize all qubits to |0>
    for q in range(n_data + n_meas):
        circuit.append("R", [q])

    # Repeat syndrome measurement rounds
    for r in range(rounds):
        # Reset measurement qubits
        for m in range(1, n_data + n_meas, 2):
            circuit.append("R", [m])
        # CNOTs for parity checks
        for i in range(n_meas):
            d1 = i * 2  # data qubit index
            m = i * 2 + 1  # measurement qubit index
            d2 = (i + 1) * 2  # next data qubit index
            circuit.append("CNOT", [d1, m])
            circuit.append("CNOT", [d2, m])
        # Measure measurement qubits
        for m in range(1, n_data + n_meas, 2):
            circuit.append("M", [m])
            circuit.append("DETECTOR", [stim.target_rec(-1)])
    # Final measurement of data qubits
    for d in range(0, n_data + n_meas, 2):
        circuit.append("M", [d])
    return circuit


def build_manual_detector_error_model():
    """
    Manually construct a detector error model for a distance-3 repetition code.
    This demonstrates the structure of a DEM without relying on stim circuit generation.
    """
    # For a distance-3 repetition code with 3 rounds:
    # - We have 2 detectors per round (detecting parity between adjacent qubits)
    # - Total of 6 detectors across 3 rounds
    # - 3 data qubits (logical observables)

    dem_instructions = []

    # Error probabilities
    p_single = 0.001  # Single qubit error probability
    p_two = 0.0001  # Two qubit error probability

    # Single qubit errors affecting detectors
    # Data qubit 0 errors affect detector 0 in each round
    for round_idx in range(3):
        detector_id = round_idx * 2  # Detector 0, 2, 4
        dem_instructions.append(f"error({p_single}) D{detector_id} L0")

    # Data qubit 1 errors affect both detectors in each round
    for round_idx in range(3):
        detector_id1 = round_idx * 2  # Detector 0, 2, 4
        detector_id2 = round_idx * 2 + 1  # Detector 1, 3, 5
        dem_instructions.append(f"error({p_single}) D{detector_id1} D{detector_id2} L1")

    # Data qubit 2 errors affect detector 1 in each round
    for round_idx in range(3):
        detector_id = round_idx * 2 + 1  # Detector 1, 3, 5
        dem_instructions.append(f"error({p_single}) D{detector_id} L2")

    # Measurement errors (affect single detectors)
    for detector_id in range(6):
        dem_instructions.append(f"error({p_single}) D{detector_id}")

    # Correlated errors between adjacent rounds
    for round_idx in range(2):
        # Detector correlations between rounds
        d1 = round_idx * 2
        d2 = (round_idx + 1) * 2
        dem_instructions.append(f"error({p_two}) D{d1} D{d2}")

        d1 = round_idx * 2 + 1
        d2 = (round_idx + 1) * 2 + 1
        dem_instructions.append(f"error({p_two}) D{d1} D{d2}")

    # Create the DEM from instructions
    dem_str = "\n".join(dem_instructions)
    dem = stim.DetectorErrorModel(dem_str)

    return dem


def demo_manual_vs_circuit_dem():
    """
    Compare manually built DEM with circuit-generated DEM
    """
    print("=== Manual DEM Demo ===")

    # 1. Manual DEM
    manual_dem = build_manual_detector_error_model()
    print("Manual DEM structure:")
    print(manual_dem)
    print()

    # 2. Circuit-generated DEM for comparison
    circuit = build_simple_repetition_code_circuit(distance=3, rounds=3)
    circuit_dem = circuit.detector_error_model(decompose_errors=True)
    print("Circuit-generated DEM:")
    print(circuit_dem)
    print()

    # 3. Use manual DEM for decoding
    manual_matching = pymatching.Matching.from_detector_error_model(manual_dem)

    # 4. Test with some example detection events
    test_syndromes = [
        [1, 0, 0, 0, 0, 0],  # Single detector firing
        [1, 1, 0, 0, 0, 0],  # Adjacent detectors
        [1, 0, 1, 0, 0, 0],  # Same detector across rounds
        [0, 1, 0, 1, 0, 1],  # Pattern across rounds
    ]

    print("Manual DEM decoding results:")
    for i, syndrome in enumerate(test_syndromes):
        correction = manual_matching.decode(syndrome)
        print(f"Syndrome {syndrome} -> Correction {correction}")

    return manual_dem, manual_matching


def main():
    # Original demo
    print("=== Original Circuit-based Demo ===")
    distance = 3
    rounds = 3
    circuit = build_simple_repetition_code_circuit(distance, rounds)

    dem = circuit.detector_error_model(decompose_errors=True)
    matching = pymatching.Matching.from_detector_error_model(dem)

    sampler = circuit.compile_detector_sampler()
    num_shots = 5  # Reduced for clarity
    det_events = sampler.sample(num_shots)

    for i, det in enumerate(det_events):
        correction = matching.decode(det)
        print(f"Shot {i}: detection events = {det}, correction = {correction}")

    print(
        "\nNote: For repetition code, the correction array indicates which data qubits to flip."
    )
    print()

    # New manual DEM demo
    demo_manual_vs_circuit_dem()


if __name__ == "__main__":
    main()
