import pickle
import sys

# Check arguments.
if len(sys.argv) < 4:
    print("Error: Missing arguments.")
    print("Usage: filter.py {-m|-t|-p} <input-unipartite-nxgraph> <output-filtered-nxgraph>")
    sys.exit(1)

import networkx as nx


# Parameters.
threshold = 0.01
neighbor_ratio = 0.9

# Load graph.
print("Loading...")
with open(sys.argv[2], "rb") as f:
    mg = pickle.load(f)
mg_nodes = mg.number_of_nodes()
print("Before: #v = {}, #e = {}".format(mg.number_of_nodes(),
                                        mg.number_of_edges()))

# Filter graph.
print("Filtering...")
g = nx.Graph()
g_nodes = 0
num_edge = 0
num_multiedge = [0, 0, 0]
for node in mg.nodes_iter():
    g.add_node(node)
    g_nodes += 1
    ratio = g_nodes / mg_nodes
    print("\r[{}{}]({:.2f}%)".format("#" * int(80*ratio),
                                     "-"*(80-int(80*ratio)),
                                     100*ratio), end="")
    total_degrees = mg.degree(node)
    edge_dist = []
    for neighbor in mg.neighbors_iter(node):
        edge_dist.append(mg.number_of_edges(node, neighbor))
        num_edge += 1
        if edge_dist[-1] == 1:
            num_multiedge[0] += 1
        elif edge_dist[-1] == 2:
            num_multiedge[1] += 1
        else:
            num_multiedge[2] += 1
    if sys.argv[1] == "-m":
        # Multiplicity > 1
        for neighbor in mg.neighbors_iter(node):
            if mg.number_of_edges(node, neighbor) > 1:
                g.add_edge(node, neighbor)
    elif sys.argv[1] == "-t":
        # Top % of multiplicity
        edge_dist = sorted(edge_dist)
        for neighbor in mg.neighbors_iter(node):
            if mg.number_of_edges(node, neighbor) >= \
                    edge_dist[int(len(edge_dist) * neighbor_ratio)]:
                g.add_edge(node, neighbor)
    elif sys.argv[1] == "-p":
        # Multiplicity proportion > threshold
        for neighbor in mg.neighbors_iter(node):
            if mg.number_of_edges(node, neighbor) / total_degrees > threshold:
                g.add_edge(node, neighbor)
    else:
        print("Error: invalid filtering mode {}.".format(sys.argv[1]))
        sys.exit(1)

print()
print("Multiplicity = 1: {}%".format(num_multiedge[0] / num_edge * 100))
print("Multiplicity = 2: {}%".format(num_multiedge[1] / num_edge * 100))
print("Multiplicity > 2: {}%".format(num_multiedge[2] / num_edge * 100))
print("After: #v = {}, #e = {}".format(g.number_of_nodes(),
                                       g.number_of_edges()))

# Save to file.
print("Saving...")
with open(sys.argv[3], "wb") as f:
    pickle.dump(g, f)
