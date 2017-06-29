import pickle
import sys

# Check arguments.
if len(sys.argv) < 3:
    print("Error: missing arguments.")
    print("Usage: nxgraph2edgelist.py <input-nxgraph> <output-edgelist-basename>")
    sys.exit(1)


# Load graph.
print("Loading...")
with open(sys.argv[1], "rb") as f:
    graph = pickle.load(f)

# Export edgelist.
print("Saving...")
with open("{}.edgelist".format(sys.argv[2]), "w") as f:
    for src, dst in graph.edges_iter():
        f.write("{} {}\n".format(src, dst))
