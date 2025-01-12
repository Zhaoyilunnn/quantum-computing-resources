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


def test_unrotated_surface_circ():
    circ = stim.Circuit.generated(
        "surface_code:unrotated_memory_z", rounds=3, distance=3
    )
    with open("unrotated_surface_circ.stim", "w") as f:
        f.write(str(circ))

    sampler = circ.compile_detector_sampler()
    print(sampler.sample(10))

    diagram = circ.diagram(type="detslice-with-ops-svg")
    with open("unrotated_surface_circ.svg", "w") as f:
        print(diagram, file=f)


def test_rotated_surface_circ():
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
    print(surface_code_tasks[0].circuit)
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
    plt.savefig("surface_code_circ_res.pdf")


if __name__ == "__main__":
    test_rotated_surface_circ()
    test_unrotated_surface_circ()
