"""
Commit id: 62099b293cf0d824ddf932421553b5589819fb6e
"""

from collections import defaultdict
from time import time

from tqec.computation.block_graph import BlockGraph
from tqec.computation.cube import ZXCube
from tqec.gallery import steane_encoding
from tqec.interop.pyzx.correlation import _find_correlation_surfaces_from_leaf
from tqec.interop.pyzx.positioned import PositionedZX

NUM_REPLICATE = 4


def construct_chain_of_steane_codes() -> BlockGraph:
    """Construct a chain of steane codes to create a larger graph for testing."""
    block_graph: BlockGraph | None = None
    graph_clone: BlockGraph | None = None
    for i in range(NUM_REPLICATE):
        g = steane_encoding()
        g.relabel_cubes({f"Port{j}": f"Port{j}_{i}" for j in range(7)})
        if block_graph is None:
            block_graph = g
        else:
            block_graph = block_graph.compose(g, f"Port4_{i - 1}", f"Port3_{i}")
        graph_clone = block_graph.clone()
        graph_clone.fill_ports(ZXCube.from_str("ZXZ"))
    assert block_graph is not None and graph_clone is not None
    return graph_clone


def test_find_correlation_surface(graph: BlockGraph):
    """Test the performance and redundancy of finding correlation surfaces from leaf nodes."""
    # 1. Convert to pyzx graph
    positioned_zx = PositionedZX.from_block_graph(graph)
    zx_g = positioned_zx.g
    p2v = positioned_zx.p2v

    # 2. Get leaf nodes
    leaf_cubes = graph.leaf_cubes
    leaves = {p2v[cube.position] for cube in leaf_cubes}
    print(f"   - Found {len(leaves)} leaf nodes in the graph.")

    print("\n2. Starting computation analysis...")

    unique_surfaces = set()
    all_surfaces_found = []

    total_computation_time = 0.0
    redundant_computation_time = 0.0
    new_discovery_time = 0.0

    # Store which leaf found which surface
    surface_to_leaf_map = defaultdict(list)

    for k, leaf in enumerate(leaves):
        print(
            f"   - Processing leaf {k + 1}/{len(leaves)} (Node ID: {leaf})...", end=""
        )

        start_time = time()
        # This is the function we want to test
        surfaces_from_this_leaf = _find_correlation_surfaces_from_leaf(zx_g, leaf)
        end_time = time()

        duration = end_time - start_time
        total_computation_time += duration

        if not surfaces_from_this_leaf:
            print(f" Found 0 surfaces in {duration:.6f} seconds. (Redundant)")
            redundant_computation_time += duration
            continue

        all_surfaces_found.extend(surfaces_from_this_leaf)

        # Check if this computation discovered any new surfaces
        is_new_discovery = False
        newly_found_count = 0
        for surface in surfaces_from_this_leaf:
            surface_to_leaf_map[surface].append(leaf)
            if surface not in unique_surfaces:
                is_new_discovery = True
                unique_surfaces.add(surface)
                newly_found_count += 1

        if is_new_discovery:
            new_discovery_time += duration
            print(
                f" Found {len(surfaces_from_this_leaf)} surfaces ({newly_found_count} new) "
                f"in {duration:.6f} seconds. (Discovery)"
            )
        else:
            redundant_computation_time += duration
            print(
                f" Found {len(surfaces_from_this_leaf)} surfaces "
                f"(0new) in {duration:.6f} seconds. (Redundant)"
            )

    print("\n3. Analysis Results:")
    print("-" * 30)

    num_total_found = len(all_surfaces_found)
    num_unique_found = len(unique_surfaces)
    num_redundant_computations = num_total_found - num_unique_found

    print(f"Total surfaces found (including duplicates): {num_total_found}")
    print(f"Unique surfaces found: {num_unique_found}")
    print(f"Number of redundant surfaces found: {num_redundant_computations}")

    print("\nPerformance Impact:")
    print(f"Total computation time: {total_computation_time:.6f} seconds")
    print(
        f"Time spent on computations yielding new surfaces: {new_discovery_time:.6f} seconds"
    )
    print(
        f"Time spent on purely redundant computations: {redundant_computation_time:.6f} seconds"
    )

    if total_computation_time > 0:
        redundancy_percentage = (
            redundant_computation_time / total_computation_time
        ) * 100
        print(
            f"Percentage of time wasted on redundant computations: {redundancy_percentage:.2f}%"
        )

    print("\nDetails of redundant findings:")
    for k, surface in enumerate(unique_surfaces):
        finders = surface_to_leaf_map[surface]
        if len(finders) > 1:
            print(
                f"  - Surface {k + 1} was found {len(finders)} times by leaves: {finders}"
            )


if __name__ == "__main__":
    print("1. Constructing a chain of Steane codes...")
    test_graph = construct_chain_of_steane_codes()
    print("   - Construction complete.\n")
    test_find_correlation_surface(test_graph)

    print("\n" + "-" * 30)
    print("4. Comparing with the original `find_correlation_surfaces` function.")
    start_time = time()
    surfaces = test_graph.find_correlation_surfaces()
    end_time = time()
    print(f"Total time taken: {end_time - start_time:.6f} seconds")
    print(f"Total number of surfaces found: {len(surfaces)}")
