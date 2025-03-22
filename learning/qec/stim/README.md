
This document aims to record some extended illustrations of the `Stim` framework.

# Circuit File Format

- `OBSERVABLE_INCLUDE`: an annotation used to declare that one or more measurement record bits should contribute to a logical observable. In other words, it marks specific measurement outcomes (indicated by the provided measurement record targets) as part of the circuit’s final logical measurement. The number in parentheses (e.g. `OBSERVABLE_INCLUDE(0)`) specifies the index of the logical observable being defined. When a simulator processes the circuit, it uses the measurement results indicated by these targets to compute the corresponding logical value (often by taking a parity over them), which can then be used in error correction or for determining the outcome of a logical qubit. This annotation is crucial in circuits where the logical observable is not measured directly but must be inferred from a combination of physical measurement outcomes.
