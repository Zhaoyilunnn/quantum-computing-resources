"""
https://github.com/tqec/tqec/commit/d5d77c27dc3989176897113d3a3925fab5585c57
"""

from tqec.compile.blocks.block import Block
from tqec.compile.blocks.layers.atomic.plaquettes import PlaquetteLayer
from tqec.compile.blocks.layers.composed.repeated import RepeatedLayer
from tqec.compile.graph import TopologicalComputationGraph
from tqec.compile.specs.library.generators.memory import (
    get_memory_horizontal_boundary_plaquettes,
    get_memory_horizontal_boundary_raw_template,
    get_memory_qubit_plaquettes,
    get_memory_qubit_raw_template,
)
from tqec.compile.tree import LayerNode
from tqec.utils.enums import Basis
from tqec.utils.position import BlockPosition3D
from tqec.utils.scale import LinearFunction, PhysicalQubitScalable2D

scalable_qubit_shape = PhysicalQubitScalable2D(
    LinearFunction(4, 5), LinearFunction(4, 5)
)

graph = TopologicalComputationGraph(scalable_qubit_shape)
XZZ = Block(
    [
        PlaquetteLayer(
            get_memory_qubit_raw_template(),
            get_memory_qubit_plaquettes(reset=Basis.Z),
        ),
        RepeatedLayer(
            PlaquetteLayer(
                get_memory_qubit_raw_template(), get_memory_qubit_plaquettes()
            ),
            repetitions=LinearFunction(2, -1),
        ),
        PlaquetteLayer(
            get_memory_qubit_raw_template(),
            get_memory_qubit_plaquettes(measurement=Basis.Z),
        ),
    ]
)
XZO = Block(
    [
        PlaquetteLayer(
            get_memory_qubit_raw_template(),
            get_memory_qubit_plaquettes(),
        )
        for _ in range(2)
    ]
)
OZZ = Block(
    [
        PlaquetteLayer(
            get_memory_horizontal_boundary_raw_template(),
            get_memory_horizontal_boundary_plaquettes(reset=Basis.Z),
        ),
        RepeatedLayer(
            PlaquetteLayer(
                get_memory_horizontal_boundary_raw_template(),
                get_memory_horizontal_boundary_plaquettes(),
            ),
            repetitions=LinearFunction(2, -1),
        ),
        PlaquetteLayer(
            get_memory_horizontal_boundary_raw_template(),
            get_memory_horizontal_boundary_plaquettes(measurement=Basis.Z),
        ),
    ]
)
graph.add_cube(BlockPosition3D(0, 0, 0), XZZ)
graph.add_cube(BlockPosition3D(1, 0, 0), XZZ)
graph.add_cube(BlockPosition3D(0, 0, 1), XZZ)
graph.add_cube(BlockPosition3D(1, 0, 1), XZZ)
graph.add_pipe(BlockPosition3D(0, 0, 0), BlockPosition3D(0, 0, 1), XZO)
graph.add_pipe(BlockPosition3D(1, 0, 0), BlockPosition3D(1, 0, 1), XZO)
graph.add_pipe(BlockPosition3D(0, 0, 1), BlockPosition3D(1, 0, 1), OZZ)


layer_tree = graph.to_layout_tree()
__import__("pprint").pprint(layer_tree.to_dict())
