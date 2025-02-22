from tqec.gallery import cnot, move_rotation
from tqec import Basis
from tqec import compile_block_graph, NoiseModel
import time

# block_graph = move_rotation(Basis.Z)
block_graph = cnot(Basis.Z)

# block_graph.view_as_html(write_html_filepath="temp.html")

correlation_surfaces = block_graph.find_correlation_surfaces()
compiled_computation = compile_block_graph(block_graph, observables="auto")

# 3. Generate the `stim.Circuit` of target code distance
start = time.perf_counter()
circuit = compiled_computation.generate_stim_circuit(
    # k = (d-1)/2 is the scale factor
    # Large values will take a lot of time.
    k=2,
    # The noise applied and noise levels can be changed.
    noise_model=NoiseModel.uniform_depolarizing(0.001),
    parallel=True,
)
print("Parallel: Generate stim circuit consumes: ", time.perf_counter() - start)

# 3. Generate the `stim.Circuit` of target code distance
start = time.perf_counter()
circuit = compiled_computation.generate_stim_circuit(
    # k = (d-1)/2 is the scale factor
    # Large values will take a lot of time.
    k=2,
    # The noise applied and noise levels can be changed.
    noise_model=NoiseModel.uniform_depolarizing(0.001),
    parallel=False,
)
print("Serial: Generate stim circuit consumes: ", time.perf_counter() - start)

diagram = circuit.diagram(type="detslice-with-ops-svg")
with open("temp.svg", "w") as f:
    print(diagram, file=f)
