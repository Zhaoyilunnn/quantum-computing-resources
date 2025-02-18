import stim
import argparse

# define a argument parser, with a positional argument for the file name
parser = argparse.ArgumentParser(description="Read and plot a stabilizer circuit.")
parser.add_argument(
    "file", type=str, help="The file to read the stabilizer circuit from."
)
args = parser.parse_args()

circ = stim.Circuit.from_file(args.file)

# diagram = circ.diagram(type="detslice-with-ops-svg", tick=range(0, 9))
# red: x-stabilizer, blue: z-stabilizer
diagram = circ.diagram(type="detslice-with-ops-svg")
with open("temp.svg", "w") as f:
    print(diagram, file=f)
