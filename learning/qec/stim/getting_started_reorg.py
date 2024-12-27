import stim
import numpy as np
import matplotlib.pyplot as plt
import sinter
import pymatching
import os
import scipy.stats
from typing import List


def count_logical_errors(circuit: stim.Circuit, num_shots: int) -> int:
    # Sample the circuit.
    sampler = circuit.compile_detector_sampler()
    detection_events, observable_flips = sampler.sample(
        num_shots, separate_observables=True
    )

    # Configure a decoder using the circuit.
    detector_error_model = circuit.detector_error_model(decompose_errors=True)
    matcher = pymatching.Matching.from_detector_error_model(detector_error_model)

    # Run the decoder.
    predictions = matcher.decode_batch(detection_events)

    # Count the mistakes.
    num_errors = 0
    for shot in range(num_shots):
        actual_for_shot = observable_flips[shot]
        predicted_for_shot = predictions[shot]
        if not np.array_equal(actual_for_shot, predicted_for_shot):
            num_errors += 1
    return num_errors


if __name__ == "__main__":
    print(stim.__version__)

    # Basic Circuit Example
    circuit = stim.Circuit()
    circuit.append("H", [0])
    circuit.append("CNOT", [0, 1])
    circuit.append("M", [0, 1])
    print(circuit)
    print(circuit.diagram())
    # print(circuit.diagram("timeline-svg"))

    sampler = circuit.compile_sampler()
    print(sampler.sample(shots=10))

    circuit.append("DETECTOR", [stim.target_rec(-1), stim.target_rec(-2)])
    print(repr(circuit))

    sampler = circuit.compile_detector_sampler()
    print(sampler.sample(shots=5))

    # Adding Noise and Sampling
    circuit = stim.Circuit(
        """
        H 0
        TICK

        CX 0 1
        X_ERROR(0.2) 0 1
        TICK

        M 0 1
        DETECTOR rec[-1] rec[-2]
    """
    )
    # print(circuit.diagram("timeslice-svg"))

    sampler = circuit.compile_detector_sampler()
    print(sampler.sample(shots=10))
    print(np.sum(sampler.sample(shots=10**6)) / 10**6)

    # Repetition Code
    circuit = stim.Circuit.generated(
        "repetition_code:memory",
        rounds=25,
        distance=9,
        before_round_data_depolarization=0.04,
        before_measure_flip_probability=0.01,
    )
    print(repr(circuit))
    # print(circuit.diagram("timeline-svg"))

    sampler = circuit.compile_sampler()
    one_sample = sampler.sample(shots=1)[0]
    for k in range(0, len(one_sample), 8):
        timeslice = one_sample[k : k + 8]
        print("".join("1" if e else "_" for e in timeslice))

    detector_sampler = circuit.compile_detector_sampler()
    one_sample = detector_sampler.sample(shots=1)[0]
    for k in range(0, len(one_sample), 8):
        timeslice = one_sample[k : k + 8]
        print("".join("!" if e else "_" for e in timeslice))

    dem = circuit.detector_error_model()
    print(repr(dem))
    # print(dem.diagram("matchgraph-svg"))

    # Logical Errors Analysis
    circuit = stim.Circuit.generated(
        "repetition_code:memory",
        rounds=100,
        distance=9,
        before_round_data_depolarization=0.03,
    )
    num_shots = 100_000
    num_logical_errors = count_logical_errors(circuit, num_shots)
    print(f"there were {num_logical_errors} wrong predictions out of {num_shots} shots")

    circuit = stim.Circuit.generated(
        "repetition_code:memory",
        rounds=100,
        distance=9,
        before_round_data_depolarization=0.13,
        before_measure_flip_probability=0.01,
    )
    num_shots = 10_000
    num_logical_errors = count_logical_errors(circuit, num_shots)
    print(f"there were {num_logical_errors} wrong predictions out of {num_shots} shots")

    # Noise vs Logical Error Rate Plot
    num_shots = 10_000
    for d in [3, 5, 7]:
        xs = []
        ys = []
        for noise in [0.1, 0.2, 0.3, 0.4, 0.5]:
            circuit = stim.Circuit.generated(
                "repetition_code:memory",
                rounds=d * 3,
                distance=d,
                before_round_data_depolarization=noise,
            )
            num_errors_sampled = count_logical_errors(circuit, num_shots)
            xs.append(noise)
            ys.append(num_errors_sampled / num_shots)
        plt.plot(xs, ys, label=f"d={d}")
    plt.loglog()
    plt.xlabel("physical error rate")
    plt.ylabel("logical error rate per shot")
    plt.legend()
    plt.show()

    # Surface Code Task Collection
    surface_code_tasks = [
        sinter.Task(
            circuit=stim.Circuit.generated(
                "surface_code:rotated_memory_z",
                rounds=d * 3,
                distance=d,
                after_clifford_depolarization=0.001,
                after_reset_flip_probability=0.001,
                before_measure_flip_probability=0.001,
                before_round_data_depolarization=0.001,
            ),
            json_metadata={"d": d, "r": d * 3, "p": 0.001},
        )
        for d in [3, 5, 7, 9]
    ]
    collected_surface_code_stats = sinter.collect(
        num_workers=int(os.cpu_count() // 2),
        tasks=surface_code_tasks,
        decoders=["pymatching"],
        max_shots=5_000_000,
        max_errors=100,
        print_progress=True,
    )

    # Logical Error Rate vs Code Distance Plot
    xs = []
    ys = []
    log_ys = []
    for stats in collected_surface_code_stats:
        d = stats.json_metadata["d"]
        if not stats.errors:
            print(f"Didn't see any errors for d={d}")
            continue
        per_shot = stats.errors / stats.shots
        per_round = sinter.shot_error_rate_to_piece_error_rate(
            per_shot, pieces=stats.json_metadata["r"]
        )
        xs.append(d)
        ys.append(per_round)
        log_ys.append(np.log(per_round))
    fit = scipy.stats.linregress(xs, log_ys)
    print(fit)

    fig, ax = plt.subplots(1, 1)
    ax.scatter(xs, ys, label="sampled logical error rate")
    ax.plot(
        [0, 25],
        [np.exp(fit.intercept), np.exp(fit.intercept + fit.slope * 25)],
        linestyle="--",
        label="least squares line fit",
    )
    ax.set_ylim(1e-12, 1e-0)
    ax.set_xlim(0, 25)
    ax.semilogy()
    ax.set_title("Projecting distance needed to survive a trillion rounds")
    ax.set_xlabel("Code Distance")
    ax.set_ylabel("Logical Error Rate per Round")
    ax.grid(which="major")
    ax.grid(which="minor")
    ax.legend()
    fig.set_dpi(120)
