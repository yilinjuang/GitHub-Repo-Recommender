import pickle
import platform
import random
import sys
import time
from collections import namedtuple
from multiprocessing import Pool

# Check arguments.
if len(sys.argv) < 4:
    print("Error: missing arguments.")
    print("Usage: bi_pred.py <input-bipartite-nxgraph> <input-data-basename> <K>")
    sys.exit(1)

import networkx as nx
import numpy as np
from scipy.sparse.linalg import svds
from networkx.algorithms import bipartite

import openblas_util as ou
N_PROC = ou.get_num_procs()
print("Number of processors: {}".format(N_PROC))
print("Number of threads: {}".format(ou.get_num_threads()))

start_time = time.time()

# Load graph.
print("Loading...")
'''
with open(sys.argv[1], "rb") as f:
    big = pickle.load(f)
print("Bipartite graph: #v = {}, #e = {}".format(big.number_of_nodes(), big.number_of_edges()))

print("Generate biadjacency matrix...")
users, repos = map(list, bipartite.sets(big))
B = bipartite.biadjacency_matrix(big, users, repos)
B = B.asfptype()
with open("{}.biadj".format(sys.argv[2]), "wb") as f:
    pickle.dump((users, repos, B), f)
'''
with open("{}.biadj".format(sys.argv[2]), "rb") as f:
    users, repos, B = pickle.load(f)

# Remove edges.
PROB_REMOVED = 0.2    # Probability whether an edge should be removed.
nonzero_user_indices, nonzero_repo_indices = B.nonzero()
print("Removing {:.4f}% edges from {}...".format(PROB_REMOVED*100, len(nonzero_user_indices)))
n_removed = 0   # Total removed edges.
nonzero_positions = set()    # set of nonzero position (u, r)
removed_positions = set()   # set of removed position (u, r)
for i, (user_index, repo_index) in enumerate(zip(nonzero_user_indices, nonzero_repo_indices)):
    pos = (user_index, repo_index)
    if random.random() < PROB_REMOVED:
        n_removed += 1
        removed_positions.add(pos)
        B[pos] = 0.0   # Remove edge.
    else:
        nonzero_positions.add(pos)
print("Removed {} edges.".format(n_removed))

# Perform singular value decomposition.
# K = 10     # Number of eigenvectors/eigenvalues of SVD
K = int(sys.argv[3])     # Number of eigenvectors/eigenvalues of SVD
print("Performing SVD with K = {}...".format(K))
U, S, V = svds(B, k=K)

# Apply pseudo kernel function.
def rank_reduction(S):
    s = S.copy()
    s[s<np.median(s)] = 0.0
    return s
print("Applying pseudo kernel function sinh and rank reduction...")
S /= np.max(S)              # Normalize S.
S_sinh = np.sinh(S)         # Apply sinh pseudo kernel.
S_rr = rank_reduction(S)    # Apply rank reduction pseudo kernel.

# Sample best results.
SAMPLE_RATE = 0.01
N_SAMPLE = int(SAMPLE_RATE * len(users) * len(repos))
N_TOP = int(n_removed * SAMPLE_RATE)
N_CHUNK = max(N_PROC, int(N_SAMPLE / 1e7 // N_PROC * N_PROC))  # Multiple of 120 (LCM of 24 and 60)
N_PER_CHUNK = N_SAMPLE // N_CHUNK   # Roughly 1e7 to control memory usage.
N_TOP_PER_CHUNK = int(N_TOP * 10 / N_CHUNK) # Total returned top results should be 10 times of N_TOP
if platform.node() == 'hp':
    N_PROCESS = 60
else:   # kdd2, kdd3
    N_PROCESS = N_PROC

def check_predict():
    Best = namedtuple("Best", ["U", "values", "min_value"])
    values = [((0, 0), 0) for _ in range(N_TOP_PER_CHUNK)]
    bests = []
    bests.append(Best(U_sinh, list(values), 0))
    bests.append(Best(U_rr, list(values), 0))
    user_indices = random.choices(range(len(users)), k=N_PER_CHUNK)
    repo_indices = random.choices(range(len(repos)), k=N_PER_CHUNK)
    for index in range(N_PER_CHUNK):
        pos = (user_indices[index], repo_indices[index])
        if pos in nonzero_positions:    # Link already exists.
            continue
        for i in range(len(bests)):
            new = bests[i].U[pos[0], :] @ V[:, pos[1]]
            if new > bests[i].min_value:
                bests[i].values.append((pos, new))
                bests[i].values.sort(key=lambda p: p[1], reverse=True)
                bests[i].values.pop()
                bests[i] = bests[i]._replace(min_value=bests[i].values[-1][1])
    for i in range(len(bests)):
        assert len(bests[i].values) == N_TOP_PER_CHUNK
    return bests[0].values, bests[1].values

def collect_predict(results):
    print("#", end="")
    sys.stdout.flush()
    top_sinh.extend(results[0])
    top_rr.extend(results[1])

print("Sampling best {} predictions with rate {:.4f}, or {} samples...".format(N_TOP, SAMPLE_RATE, N_SAMPLE))
U_sinh = U * S_sinh
U_rr = U * S_rr
top_sinh = []     # [((u, v), b_value), (), ...]
top_rr = []     # [((u, v), b_value), (), ...]
print("=" * N_CHUNK)
with Pool(processes=N_PROCESS) as pool:
    results = [pool.apply_async(check_predict, callback=collect_predict) for _ in range(N_CHUNK)]
    for r in results:
        r.wait()
assert len(top_sinh) == N_CHUNK * N_TOP_PER_CHUNK
assert len(top_rr) == N_CHUNK * N_TOP_PER_CHUNK
top_sinh.sort(key=lambda p: p[1], reverse=True)
top_rr.sort(key=lambda p: p[1], reverse=True)
top_sinh = top_sinh[:N_TOP]
top_rr = top_rr[:N_TOP]

# Evaluation.
print("\nEvaluating...")
correct_sinh = 0
for pred in top_sinh:
    if pred[0] in removed_positions:
        correct_sinh += 1
correct_rr = 0
for pred in top_rr:
    if pred[0] in removed_positions:
        correct_rr += 1

# Save result.
output_sinh = "Accuracy = {:.4f}% ({}/{}), K = {}, kernel = sinh".format(correct_sinh/N_TOP*100, correct_sinh, N_TOP, K)
output_rr = "Accuracy = {:.4f}% ({}/{}), K = {}, kernel = rr".format(correct_rr/N_TOP*100, correct_rr, N_TOP, K)
output = "{}\n{}, time = {:.0f}s".format(output_sinh, output_rr, time.time()-start_time)
with open("{}.log".format(sys.argv[2]), "a") as f:
    f.write("{}\n".format(output))
print(output)
