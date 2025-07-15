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


class UniversalQECAdapter:
    """
    Universal quantum error correction adapter that interfaces with pymatching
    without depending on stim circuit generation.
    """

    def __init__(self, distance=3, rounds=3, code_type="repetition"):
        self.distance = distance
        self.rounds = rounds
        self.code_type = code_type
        self.num_detectors = self._calculate_num_detectors()
        # For demo purposes, use a simple direct matching approach

    def _calculate_num_detectors(self):
        """Calculate number of detectors based on code parameters"""
        if self.code_type == "repetition":
            return (self.distance - 1) * self.rounds
        else:
            raise ValueError(f"Unsupported code type: {self.code_type}")

    def simulate_syndromes(self, num_shots=100, error_rate=0.01):
        """
        Simulate syndrome data without actual quantum circuit.
        This could be replaced with data from any quantum simulator.
        """
        syndromes = []
        for _ in range(num_shots):
            # Generate random syndrome with some probability
            syndrome = np.random.binomial(1, error_rate, size=self.num_detectors)
            syndromes.append(syndrome)
        return np.array(syndromes)

    def process_raw_measurements(self, raw_data):
        """
        Process raw measurement data from external simulator.
        raw_data: array of shape (shots, num_qubits) with measurement outcomes
        """
        syndromes = []
        for shot in raw_data:
            syndrome = []
            # Calculate parity checks for repetition code
            for round_idx in range(self.rounds):
                for det_idx in range(self.distance - 1):
                    # Parity between adjacent data qubits
                    q1 = det_idx * 2  # Data qubit positions: 0, 2, 4, ...
                    q2 = (det_idx + 1) * 2
                    if q1 < len(shot) and q2 < len(shot):
                        parity = (shot[q1] + shot[q2]) % 2
                        syndrome.append(parity)
                    else:
                        syndrome.append(0)  # Default if not enough qubits
            syndromes.append(syndrome)
        return np.array(syndromes)

    def simple_decode(self, syndrome):
        """
        Simple decoding logic for repetition code without full matching.
        This demonstrates the concept - in practice you'd use pymatching.
        """
        correction = np.zeros(self.distance, dtype=int)

        # Simple majority vote decoding for repetition code
        for data_qubit in range(self.distance):
            error_count = 0
            total_checks = 0

            # Count how many detectors suggest this qubit has an error
            for round_idx in range(self.rounds):
                if data_qubit == 0:
                    # Left boundary: only affects first detector
                    det_idx = round_idx * (self.distance - 1)
                    if det_idx < len(syndrome):
                        error_count += syndrome[det_idx]
                        total_checks += 1
                elif data_qubit == self.distance - 1:
                    # Right boundary: only affects last detector
                    det_idx = round_idx * (self.distance - 1) + (self.distance - 2)
                    if det_idx < len(syndrome):
                        error_count += syndrome[det_idx]
                        total_checks += 1
                else:
                    # Middle qubits: affects two detectors
                    det1 = round_idx * (self.distance - 1) + (data_qubit - 1)
                    det2 = round_idx * (self.distance - 1) + data_qubit
                    if det1 < len(syndrome) and det2 < len(syndrome):
                        # Both detectors should fire for middle qubit error
                        if syndrome[det1] and syndrome[det2]:
                            error_count += 2
                        total_checks += 2

            # Simple threshold: if more than half the checks suggest error
            if total_checks > 0 and error_count > total_checks / 2:
                correction[data_qubit] = 1

        return correction

    def decode_batch(self, syndromes):
        """Decode a batch of syndromes using simple decoder"""
        corrections = []
        for syndrome in syndromes:
            correction = self.simple_decode(syndrome)
            corrections.append(correction)
        return np.array(corrections)


def demo_universal_adapter():
    """
    Demonstrate the universal QEC adapter that works without stim
    """
    print("=== Universal QEC Adapter Demo ===")

    # Initialize adapter
    adapter = UniversalQECAdapter(distance=3, rounds=3, code_type="repetition")
    print(f"Adapter initialized: {adapter.distance}-distance repetition code")
    print(f"Number of detectors: {adapter.num_detectors}")
    print()

    # Test 1: Simulate syndromes directly
    print("Test 1: Direct syndrome simulation")
    syndromes = adapter.simulate_syndromes(num_shots=5, error_rate=0.1)
    corrections = adapter.decode_batch(syndromes)

    for i, (syndrome, correction) in enumerate(zip(syndromes, corrections)):
        print(f"Shot {i}: syndrome={syndrome} -> correction={correction}")
    print()

    # Test 2: Process "raw" measurement data (simulated)
    print("Test 2: Raw measurement processing")
    # Simulate raw measurement data from external simulator
    num_qubits = adapter.distance + adapter.distance - 1  # data + ancilla qubits
    raw_measurements = np.random.binomial(1, 0.05, size=(3, num_qubits))

    print("Simulated raw measurements (from external simulator):")
    for i, raw in enumerate(raw_measurements):
        print(f"Shot {i}: raw_data={raw}")

    # Process into syndromes
    processed_syndromes = adapter.process_raw_measurements(raw_measurements)
    processed_corrections = adapter.decode_batch(processed_syndromes)

    print("\nProcessed syndromes and corrections:")
    for i, (syndrome, correction) in enumerate(
        zip(processed_syndromes, processed_corrections)
    ):
        print(f"Shot {i}: syndrome={syndrome} -> correction={correction}")
    print()

    # Test 3: Comparison with manual test cases
    print("Test 3: Manual test cases")
    test_cases = [
        [1, 0, 0, 0, 0, 0],  # Single detector
        [1, 1, 0, 0, 0, 0],  # Adjacent detectors (middle qubit error)
        [1, 0, 1, 0, 0, 0],  # Same position across rounds
        [0, 1, 0, 1, 0, 1],  # Pattern indicating correlated errors
    ]

    for i, test_syndrome in enumerate(test_cases):
        correction = adapter.simple_decode(test_syndrome)
        print(f"Test {i}: syndrome={test_syndrome} -> correction={correction}")

    print("\nUniversal adapter successfully demonstrates QEC without stim!")
    print("This adapter can work with any quantum simulator by:")
    print("1. Implementing custom syndrome simulation in simulate_syndromes()")
    print("2. Processing raw simulator data in process_raw_measurements()")
    print("3. Using simple decoding logic (or integrating with pymatching)")
    print("4. Easily extensible to other quantum simulators (Qiskit, Cirq, etc.)")

    return adapter


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

    # Universal adapter demo
    demo_universal_adapter()


if __name__ == "__main__":
    main()
