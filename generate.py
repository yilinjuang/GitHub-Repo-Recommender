# NetworkX reference: https://networkx.readthedocs.io/en/stable/reference/algorithms.bipartite.html

import pickle
import sys

# Check arguments.
if len(sys.argv) != 3:
    print("Error: Missing arguments.")
    print("Usage: generate.py <input-data-basename> <output-multigraph-basename>")
    sys.exit(1)

import networkx as nx
from networkx.algorithms import bipartite


# Load graph.
print("Loading...")
with open("{}.user".format(sys.argv[1]), "rb") as f:
    user_id2name = pickle.load(f)
    users = set(user_id2name.keys())
with open("{}.repo".format(sys.argv[1]), "rb") as f:
    repo_id2name = pickle.load(f)
    repos = set(repo_id2name.keys())
with open("{}.edge".format(sys.argv[1]), "rb") as f:
    edges = pickle.load(f)
print("users = {}, repos = {}, edges = {}"\
        .format(len(users), len(repos), len(edges)))

# Build bipartite graph.
print("Building...")
bi_graph = nx.Graph()
bi_graph.add_nodes_from(list(users), bipartite=0)
bi_graph.add_nodes_from(list(repos), bipartite=1)
bi_graph.add_edges_from(edges)

# Project to unipartite graph.
# print("Projecting...")
# # user_graph = bipartite.projected_graph(bi_graph, list(users))
# # repo_graph = bipartite.projected_graph(bi_graph, list(repos))
# user_multi_graph = bipartite.projected_graph(bi_graph, list(users), multigraph=True)
# repo_multi_graph = bipartite.projected_graph(bi_graph, list(repos), multigraph=True)

# Save to file.
print("Saving...")
with open("{}_bi.nxgraph".format(sys.argv[2]), "wb") as f:
    pickle.dump(bi_graph, f)
# with open("{}_usermulti.nxgraph".format(sys.argv[2]), "wb") as f:
    # pickle.dump(user_multi_graph, f)
# with open("{}_repomulti.nxgraph".format(sys.argv[2]), "wb") as f:
    # pickle.dump(repo_multi_graph, f)
