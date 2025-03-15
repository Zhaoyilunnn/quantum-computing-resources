from tqec import BlockGraph, ZXCube, Cube, Position3D

g = BlockGraph("Single Block Spatial Cube Test")
g.add_node(Cube(Position3D(0, 0, 0), ZXCube.from_str("XXZ")))

g.view_as_html(write_html_filepath="single_block_spatial_cube_test.html")
