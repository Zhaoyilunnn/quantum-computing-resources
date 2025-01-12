import stim

circ = stim.Circuit.from_file("./example_lattice_surgery.txt")

# diagram = circ.diagram(type="detslice-with-ops-svg", tick=range(0, 9))
# red: x-stabilizer, blue: z-stabilizer
diagram = circ.diagram(type="detslice-with-ops-svg")
with open("temp.svg", "w") as f:
    print(diagram, file=f)


sampler = circ.compile_sampler()
print(sampler.sample(10))

sampler = circ.compile_detector_sampler()
print(sampler.sample(10))
