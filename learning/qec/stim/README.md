This document aims to record some extended illustrations of the `Stim` framework.

# Circuit File Format

- `OBSERVABLE_INCLUDE`: an annotation used to declare that one or more measurement record bits should contribute to a logical observable. In other words, it marks specific measurement outcomes (indicated by the provided measurement record targets) as part of the circuit’s final logical measurement. The number in parentheses (e.g. `OBSERVABLE_INCLUDE(0)`) specifies the index of the logical observable being defined. When a simulator processes the circuit, it uses the measurement results indicated by these targets to compute the corresponding logical value (often by taking a parity over them), which can then be used in error correction or for determining the outcome of a logical qubit. This annotation is crucial in circuits where the logical observable is not measured directly but must be inferred from a combination of physical measurement outcomes.

# Internal Data Structures in Stim

Understanding the internal data structures of Stim.

## `SparseUnsignedRevFrameTracker`

**Purpose:**  
Tracks how Pauli errors (X, Z, or both) propagate through a quantum circuit, enabling efficient error analysis and detector error model extraction.

**Design Principles:**  

- **Sparse:** Only stores the relevant connections—most qubits only affect a few detectors or observables, so memory and computation are saved.
- **Unsigned:** Tracks which errors (X, Z) are present, but not their sign (phase).
- **Reverse:** Operates by undoing gates in reverse order, tracing error propagation from measurements back to the start of the circuit.

**How it works:**  

- For each qubit, keeps a list of which error terms (detectors, observables) are sensitive to X or Z errors on that qubit.
- For each classical measurement bit, tracks which error terms depend on errors on it. If a measurement result is flipped due to noise, the tracker records which detectors or logical observables would be impacted.
- As the circuit is processed backwards, these lists are updated to reflect how each operation changes error sensitivity.
- Handles logical observables (via `OBSERVABLE_INCLUDE`) and can detect non-deterministic error propagation (anticommutation).

**Code-level usage and functionality:**  

- The tracker is instantiated with the number of qubits and initial counts of measurements and detectors.
- As the error analysis runs, gates are "undone" one by one using methods like `undo_gate`, which update the internal state (`xs`, `zs`, `rec_bits`) to reflect how errors propagate.
- For measurement gates (e.g., MX, MZ), the tracker updates which detectors/observables are affected by possible errors in the measurement result.
- For Clifford gates (e.g., CX, H), the tracker updates the error dependencies according to the gate's action on Pauli operators.
- For logical observables, the tracker updates the mapping between qubits/measurement bits and logical outcomes.
- The tracker supports efficient handling of repeated circuit blocks (loops) and can detect when a detector or observable becomes non-deterministic due to error propagation.
- At any point, you can query the tracker to see which errors could affect a given detector or observable, enabling construction of the detector error model.

**What does "detector or observable becomes non-deterministic due to error propagation" mean?**

If errors propagate in such a way that the outcome of a detector or logical observable could randomly flip (for example, due to an error that anti-commutes with the measurement or logical operator), then the result is not guaranteed—it is "non-deterministic." This situation is problematic for error correction, because you cannot trust the detector or observable to reflect the true error syndrome or logical value.

In Stim, the tracker can detect when this happens and either record it or raise an error, depending on configuration.

**Example code snippets:**

Below are some simplified code snippets to illustrate how non-determinism is detected and handled in Stim.

```cpp
// Example: Detecting non-deterministic detectors in SparseUnsignedRevFrameTracker
void SparseUnsignedRevFrameTracker::handle_gauge(
    SpanRef<const DemTarget> sorted, const CircuitInstruction &inst, GateTarget location) {
    if (sorted.empty()) {
        return;
    }
    for (const auto &d : sorted) {
        anticommutations.insert({d, location});
    }
    if (fail_on_anticommute) {
        fail_due_to_anticommutation(inst);
    }
}
```

```cpp
// Example: Undoing a measurement and checking for non-determinism
void SparseUnsignedRevFrameTracker::undo_MX(const CircuitInstruction &dat) {
    handle_z_gauges(dat); // Check for Z error gauges (non-determinism)
    for (size_t k = dat.targets.size(); k-- > 0;) {
        auto q = dat.targets[k].qubit_value();
        num_measurements_in_past--;
        auto f = rec_bits.find(num_measurements_in_past);
        if (f != rec_bits.end()) {
            xs[q].xor_sorted_items(f->second.range());
            rec_bits.erase(f);
        }
    }
}
```

If `handle_z_gauges` finds that a detector or observable is affected by a Z error that anti-commutes with the X measurement, it will record this as a non-deterministic event and, if configured, throw an error.

**Why this matters:**
This structure allows Stim to efficiently answer questions like:

- “If an X error occurs on qubit 5, which detectors or logical observables could be affected?”
- “How do errors propagate through repeated circuit blocks or complex gate sequences?”
- “Are there any detectors or observables whose outcomes are fundamentally unreliable due to error propagation?”

## `ErrorAnalyzer`

### The Role of `check_for_gauge`

The function `check_for_gauge` is a key part of Stim's error analysis process. Its main purpose is to detect when a set of detectors or observables forms a "gauge degree of freedom"—that is, when the circuit's behavior becomes non-deterministic due to anti-commutation with resets or measurements.

**Usage Scenario:**  

- After undoing certain gates (such as resets or measurements), the error tracker checks if any detectors or observables remain sensitive to errors that should have been collapsed.
- If such a set is non-empty, it means there is a non-deterministic effect (a gauge), which may or may not be allowed depending on the configuration.
- If gauge detectors are allowed, `check_for_gauge` will remove the gauge by introducing a random error mechanism.
- If not allowed, it throws a detailed exception with debugging information, including which qubits and detectors are involved, and instructions for visualizing the issue.

**Why is this important?**  
This function ensures that the output detector error model is valid and deterministic unless explicitly permitted to include random (gauge) detectors. It provides extensive debugging information to help users understand and fix issues in their quantum circuits, making it easier to identify and resolve sources of non-determinism.
