from tqec import BlockGraph, Cube, Position3D, ZXCube, SignedDirection3D, Direction3D

g = BlockGraph()
g.add_edge(
    Cube(Position3D(0, 0, 0), ZXCube.from_str("ZXZ")),
    Cube(Position3D(0, 0, 1), ZXCube.from_str("XZX")),
)
correlation_surfaces = g.to_zx_graph().find_correration_surfaces()
g.view_as_html(
    pop_faces_at_direction=SignedDirection3D(Direction3D.Y, False),
    show_correlation_surface=correlation_surfaces[0],
)
