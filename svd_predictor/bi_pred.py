# https://docs.scipy.org/doc/scipy-0.19.0/reference/generated/scipy.sparse.linalg.svds.html#scipy.sparse.linalg.svds

import pickle
import random
import sys
from multiprocessing import Pool

# Check arguments.
if len(sys.argv) < 3:
    print("Error: missing arguments.")
    print("Usage: bi_pred.py <input-bipartite-nxgraph> <input-data-basename>")
    sys.exit(1)

import networkx as nx
import numpy as np
from scipy import sparse
from networkx.algorithms import bipartite


# Load graph.
print("Loading...")
# with open(sys.argv[1], "rb") as f:
    # big = pickle.load(f)
# print("Before: #v = {}, #e = {}".format(big.number_of_nodes(), big.number_of_edges()))

# print("Generate biadjacency matrix...")
# users, repos = map(list, bipartite.sets(big))
# B = bipartite.biadjacency_matrix(big, users, repos)
# B = B.asfptype()
# with open("{}.biadj".format(sys.argv[2]), "wb") as f:
    # pickle.dump((users, repos, B), f)
with open("{}.biadj".format(sys.argv[2]), "rb") as f:
    users, repos, B = pickle.load(f)
print("SVD...")
K = 100
U, S, V = sparse.linalg.svds(B, k=K)
# U, S, V = sparse.linalg.svds(B, k=min(B.shape)-1)

# Apply kernel function.
print("Applying kernel function...")
def rr(S):  # rank reduction
    S[S<np.median(S)] = 0.0
    return S
# p_kernel = np.sinh
p_kernel = rr
S = p_kernel(S/np.max(S))
U *= S

def check_predict(_):
    print("#", end="")
    sys.stdout.flush()
    max_b = 0
    user_indices = random.choices(range(len(users)), k=N_PER_CHUNK)
    repo_indices = random.choices(range(len(repos)), k=N_PER_CHUNK)
    for index in range(N_PER_CHUNK):
        if B[user_indices[index], repo_indices[index]] == 1.0:  # Link already exists.
            continue
        new_b = U[user_indices[index], :] @ V[:, repo_indices[index]]
        if new_b > max_b:
            max_b = new_b
            user_id = users[user_indices[index]]
            repo_id = repos[repo_indices[index]]
            best_pred = (user_id, user_id2name[user_id],
                         repo_id, repo_id2name[repo_id],
                         new_b)
    # print(best_pred)
    return best_pred

with open("{}.user".format(sys.argv[2]), "rb") as f:
    user_id2name = pickle.load(f)
with open("{}.repo".format(sys.argv[2]), "rb") as f:
    repo_id2name = pickle.load(f)

N_PRED = int(1e9)
N_CHUNK = 600
N_PER_CHUNK = N_PRED // N_CHUNK
N_PROCESS = 16
best_preds = []
print("Evaluating...")
print("=" * N_CHUNK)
with Pool(processes=N_PROCESS) as pool:
    for result in pool.imap_unordered(check_predict, range(N_CHUNK), N_CHUNK//N_PROCESS):
        best_preds.append(result)
best_preds = sorted(best_preds, key=lambda p: p[4], reverse=True)
print("\nTop {} predictions / {} random samples.".format(len(best_preds), N_PRED))

# Save to file.
print("Saving...")
with open("{}_{}_K{}.pred".format(sys.argv[2], p_kernel.__name__, K), "wb") as f:
    pickle.dump(best_preds, f)
with open("{}_{}_K{}.txt".format(sys.argv[2], p_kernel.__name__, K), "w") as f:
    for uid, uname, rid, rname, v in best_preds:
        f.write("{:<20}\t{:<40}\t{}\n".format(uname, rname, v))
