import pickle
import sys

# Check arguments.
if len(sys.argv) < 3:
    print("Error: Missing arguments.")
    print("Usage: generate.py <input-data-basename> <output-graph-basename> [-p|--project]")
    sys.exit(1)

import networkx as nx
from networkx.algorithms import bipartite


# Load data.
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
print("Building bipartite graph...")
bi_graph = nx.Graph()
bi_graph.add_nodes_from(list(users), bipartite=0)
bi_graph.add_nodes_from(list(repos), bipartite=1)
bi_graph.add_edges_from(edges)
with open("{}_bi.nxgraph".format(sys.argv[2]), "wb") as f:
    pickle.dump(bi_graph, f)

# Project to unipartite graph.
if len(sys.argv) < 4 or not sys.argv[3] in ["-p", "--project"]:
    sys.exit(0)
print("Projecting to unipartite graph...")
user_graph = bipartite.projected_graph(bi_graph, list(users), multigraph=True)
repo_graph = bipartite.projected_graph(bi_graph, list(repos), multigraph=True)
with open("{}_user.nxgraph".format(sys.argv[2]), "wb") as f:
    pickle.dump(user_graph, f)
with open("{}_repo.nxgraph".format(sys.argv[2]), "wb") as f:
    pickle.dump(repo_graph, f)
