# Integration of Stim and PyMatching: Detector Error Model Generation and Matching Graph Construction

## Stim: Generation of Detector Error Model (DEM)

Stim takes a quantum circuit (stim.Circuit) as input, which includes quantum gates, noise instructions (like `X_ERROR`, `DEPOLARIZE1`), measurement instructions, and explicit detector definitions (`DETECTOR`). The goal is to convert this circuit into a Detector Error Model (DEM), which is a simplified probabilistic model describing the relationship between physical errors, triggered detectors, and logical observables.

Stim does not simulate errors forward through the circuit. Instead, it uses a reverse-tracking algorithm to determine, for each possible error location, which detectors and logical observables would be affected. This is achieved by maintaining, for each qubit at each point in the circuit, a set of "error sensitivities"—collections of detectors and logical observables that would be flipped if an error occurred at that location.

The process works as follows:

1. **Reverse Traversal**: Stim traverses the circuit backwards, starting from the end and moving towards the beginning. For each instruction, it updates the error sensitivities of the qubits involved, according to the inverse effect of the instruction.

2. **Error Sensitivity Tracking**: For each qubit, two main sensitivity sets are maintained:
   - `xs[q]`: Sensitivity to Z errors (i.e., which detectors/observables are flipped by a Z error on qubit q at this point).
   - `zs[q]`: Sensitivity to X errors (i.e., which detectors/observables are flipped by an X error on qubit q at this point).
   - Sensitivity to Y errors is implicitly given by the XOR of the above two.

3. **Gate Handling**: Each gate has a specific rule for how it transforms error sensitivities. For example, a `CX` gate will propagate X and Z sensitivities between control and target qubits in a specific way.

4. **Measurement and Detector Handling**:
   - When a `DETECTOR` instruction is encountered, a new detector is defined. The error sensitivities are updated so that any error that can flip the measurement result associated with this detector is recorded as affecting this detector.
   - When a measurement instruction is encountered, the current error sensitivities are used to update which errors can flip the measurement result, and thus which detectors are affected.

5. **Noise Instruction Handling**: When a noise instruction (e.g., `X_ERROR(p) q`) is encountered, the current error sensitivity for the relevant qubit is used to determine which detectors and logical observables are affected by an error at that location. This information is recorded as an `error(p) ...` entry in the DEM.

6. **DEM Output**: The final DEM consists of a list of `error(p) D... L...` instructions, where each instruction specifies the probability of the error, the detectors triggered, and the logical observables flipped.

The DEM can be output as a text file or as a Python object. Each `error` entry in the DEM is independent and describes a possible error event, its probability, and its consequences.

---

Details

### 1. **Entry Point**

The process starts with a call to the static method:

```cpp
DetectorErrorModel ErrorAnalyzer::circuit_to_detector_error_model(const Circuit &circuit, ...);
```

This is the main API for converting a `Circuit` into a `DetectorErrorModel`.

---

### 2. **ErrorAnalyzer Construction**

Inside this method, an `ErrorAnalyzer` object is constructed:

```cpp
ErrorAnalyzer analyzer(...);
analyzer.current_circuit_being_analyzed = &circuit;
```

---

### 3. **Reverse Traversal**

The core of the process is:

```cpp
analyzer.undo_circuit(circuit);
```

- This method traverses the circuit **backwards**.
- For each instruction, it calls the corresponding `undo_*` method (e.g., `undo_X_ERROR`, `undo_MZ`, etc.).
- These methods update the error sensitivity tracker and accumulate error information.

---

### 4. **Post-Processing**

After the traversal:

```cpp
analyzer.post_check_initialization();
```

- This checks for any remaining error sensitivities that would indicate non-deterministic behavior at the start of the circuit.

---

### 5. **Flushing Errors**

Then:

```cpp
analyzer.flush();
```

- This moves the accumulated error information from the analyzer's internal map into the `flushed_reversed_model` (a `DetectorErrorModel` built in reverse order).

---

### 6. **Reversing the Model**

Finally:

```cpp
uint64_t t = 0;
std::set<DemTarget> seen;
return unreversed(analyzer.flushed_reversed_model, t, seen);
```

- The `unreversed` function reverses the order of the error model instructions (since they were accumulated backwards) and returns the final `DetectorErrorModel`.

---

## **Summary Diagram**

```
circuit_to_detector_error_model
    └── constructs ErrorAnalyzer
        └── undo_circuit (reverse traversal)
            └── undo_* methods (update sensitivities, accumulate errors)
        └── post_check_initialization
        └── flush (move errors to flushed_reversed_model)
        └── unreversed (reverse and return DetectorErrorModel)
```

---

## **Key Files/Functions Involved**

- `ErrorAnalyzer::circuit_to_detector_error_model` (entry point)
- `ErrorAnalyzer::undo_circuit` (reverse traversal)
- `ErrorAnalyzer::undo_*` methods (per-instruction logic)
- `ErrorAnalyzer::flush` (finalize error model)
- `unreversed` (reverse the error model for output)

---

## PyMatching: Construction of Matching Graph from DEM

PyMatching uses the DEM generated by Stim to construct a matching graph, which is used for minimum-weight perfect matching (MWPM) decoding.

The process is as follows:

1. **Python Interface**: The user provides a `stim.DetectorErrorModel` object to PyMatching, typically via `Matching.from_detector_error_model(model)`. This method converts the DEM to its string representation and passes it to the C++ backend.

2. **C++ Parsing and Edge Extraction**: The C++ backend parses the DEM string using Stim's C++ library. It iterates over each `error` instruction in the DEM.

3. **Edge Construction**:
   - For each `error(p) ...` instruction, the backend extracts the list of detectors and logical observables affected.
   - If the error involves two detectors, an edge is added between the corresponding nodes in the matching graph. If the error involves one detector, an edge is added between that detector and a boundary node.
   - The edge is assigned a weight based on the error probability (typically using the log-likelihood ratio: `weight = log((1-p)/p)`).
   - The edge is annotated with any logical observables that are flipped by the error.

4. **Edge Merging**: If multiple errors connect the same pair of detectors (or the same detector to the boundary), the edges are merged according to a specified strategy (e.g., assuming independent errors).

5. **Graph Representation**: The resulting matching graph consists of nodes (detectors), edges (possible error events), and edge attributes (weight, logical observables). This graph is used by the MWPM algorithm to decode observed detection events.

6. **Decoding**: When a syndrome (set of triggered detectors) is observed, the MWPM algorithm finds the minimum-weight set of edges that could explain the syndrome, taking into account the edge weights and logical observables.

## File and Data Flow

- The user defines a quantum circuit in Stim and generates a DEM using `circuit.detector_error_model(decompose_errors=True)`.
- The DEM is passed to PyMatching, which parses it and constructs the matching graph.
- The matching graph is used for decoding detection events.

This integration allows users to go from a physical circuit description to a decoding-ready matching graph in a fully automated way, leveraging Stim's error analysis and PyMatching's efficient decoding algorithms.
