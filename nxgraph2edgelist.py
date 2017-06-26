import pickle
import sys

# Check arguments.
if len(sys.argv) != 3:
    print("Error: Missing arguments.")
    print("Usage: nxgraph2edgelist.py <input-nxgraph> <output-edgelist-basename>")
    sys.exit(1)

import networkx as nx


# Load graph.
print("Loading...")
with open(sys.argv[1], "rb") as f:
    graph = pickle.load(f)

# Export edgelist.
print("Saving...")
with open("{}.edgelist".format(sys.argv[2]), "w") as f:
    for src, dst in graph.edges_iter():
        f.write("{} {}\n".format(src, dst))

# Renumber.
'''
print("Renumbering and saving...")
id2newid = {}
newid2id = {}
newid = 1
with open("{}_rn.edgelist".format(sys.argv[2]), "w") as f:
    for src, dst in graph.edges_iter():
        if not src in id2newid:
            id2newid[src] = newid
            newid2id[newid] = src
            newid += 1
        src = id2newid[src]
        if not dst in id2newid:
            id2newid[dst] = newid
            newid2id[newid] = dst
            newid += 1
        dst = id2newid[dst]
        f.write("{} {}\n".format(src, dst))
graph.remove_nodes_from(nx.isolates(graph))
assert graph.number_of_nodes()+1 == newid
assert len(id2newid) == len(newid2id)
with open("{}_rn.idmap".format(sys.argv[2]), "wb") as f:
    pickle.dump((id2newid, newid2id), f)
'''
