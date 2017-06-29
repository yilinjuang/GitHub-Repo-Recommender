import pickle
import sys


# Check arguments.
if len(sys.argv) < 3:
    print("Error: Missing arguments.")
    print("Usage: whatsthisrepoid.py <input-log-file> <input-repo-data-file>")
    sys.exit(1)

with open(sys.argv[2], "rb") as f:
    repo_id2name = pickle.load(f)

with open(sys.argv[1], "r") as f:
    for line in f:
        comma_splits = line.strip(" \n").split(",")
        if len(comma_splits) != 2:
            continue
        repo, score = comma_splits
        repo_id = int(repo.strip(" \n").split(" ")[1])
        score = float(score.strip(" \n").split(" ")[-1])
        repo_name = repo_id2name[repo_id]
        if score == 0.0:
            print("Starred repo:    {:<50s}".format(repo_name))
        else:
            print("To-star repo:    {:<50s}{:.4f}".format(repo_name, score))
