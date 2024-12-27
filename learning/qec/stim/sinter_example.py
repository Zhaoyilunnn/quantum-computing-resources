import stim
import sinter
import matplotlib.pyplot as plt


# Generates surface code circuit tasks using Stim's circuit generation.
def generate_example_tasks():
    for p in [0.001, 0.005, 0.01]:
        for d in [3, 5]:
            yield sinter.Task(
                circuit=stim.Circuit.generated(
                    rounds=d,
                    distance=d,
                    after_clifford_depolarization=p,
                    code_task=f"surface_code:rotated_memory_x",
                ),
                json_metadata={
                    "p": p,
                    "d": d,
                },
            )


def main():
    # Collect the samples (takes a few minutes).
    samples = sinter.collect(
        num_workers=4,
        max_shots=1_000_000,
        max_errors=1000,
        tasks=generate_example_tasks(),
        decoders=["pymatching"],
    )

    # Print samples as CSV data.
    print(sinter.CSV_HEADER)
    for sample in samples:
        print(sample.to_csv_line())

    # Render a matplotlib plot of the data.
    fig, ax = plt.subplots(1, 1)
    sinter.plot_error_rate(
        ax=ax,
        stats=samples,
        group_func=lambda stat: f"Rotated Surface Code d={stat.json_metadata['d']}",
        x_func=lambda stat: stat.json_metadata["p"],
    )
    ax.loglog()
    ax.set_ylim(1e-5, 1)
    ax.grid()
    ax.set_title("Logical Error Rate vs Physical Error Rate")
    ax.set_ylabel("Logical Error Probability (per shot)")
    ax.set_xlabel("Physical Error Rate")
    ax.legend()

    # Save to file and also open in a window.
    fig.savefig("sinter_example.pdf")
    # plt.show()


# NOTE: This is actually necessary! If the code inside 'main()' was at the
# module level, the multiprocessing children spawned by sinter.collect would
# also attempt to run that code.
if __name__ == "__main__":
    main()
