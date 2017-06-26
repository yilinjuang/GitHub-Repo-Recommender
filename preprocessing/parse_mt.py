# https://developer.github.com/v3/activity/events/types/#memberevent
# https://docs.python.org/3.6/library/multiprocessing.html

import json
import os
import pickle
import sys
from multiprocessing import Pool


# Check arguments.
if len(sys.argv) != 3:
    print("Error: Missing arguments.")
    print("Usage: parse.py {<input-json-directory>, <input-json-file>} <output-data-basename>")
    sys.exit(1)

def parse_files(filename):
    # Mappings.
    user_id2name = {}
    repo_id2name = {}
    user_repo_edges = []
    print(filename)
    with open(filename, "r") as f:
        lines = f.readlines()
    for line in lines:
        data = json.loads(line)
        # if data["type"] == "MemberEvent" and data["payload"]["action"] == "added":
        if data["type"] == "WatchEvent":
            actor_name = data["actor"]["login"]
            actor_id = str(data["actor"]["id"])
            # member_name = data["payload"]["member"]["login"]
            # member_id = str(data["payload"]["member"]["id"])
            repo_name = data["repo"]["name"]
            repo_id = data["repo"]["id"]
            if not actor_id in user_id2name:
                user_id2name[actor_id] = actor_name
            # if not member_id in user_id2name:
                # user_id2name[member_id] = member_name
            if not repo_id in repo_id2name:
                repo_id2name[repo_id] = repo_name
            user_repo_edges.append((actor_id, repo_id))
            # user_repo_edges.append((member_id, repo_id))
    return user_id2name, repo_id2name, user_repo_edges

# Collect files.
in_file = sys.argv[1]
if os.path.isdir(in_file):
    files = [os.path.join(in_file, f) for f in os.listdir(in_file) if os.path.splitext(f)[-1] == ".json"]
else:
    files = [in_file]
# print("Files: {}".format(", ".join(files)))
print("{} files.".format(len(files)))

# Mappings.
user_id2name = {}
repo_id2name = {}
user_repo_edges = []

n_process = 30
with Pool(processes=n_process) as pool:
    # result = [ (user_id2name, repo_id2name, user_repo_edges), (), ..., () ]
    for result in pool.imap_unordered(parse_files, files, len(files)//n_process):
        user_id2name = {**user_id2name, **result[0]}
        repo_id2name = {**repo_id2name, **result[1]}
        user_repo_edges += result[2]
print("Users: {}".format(len(user_id2name)))
print("Repos: {}".format(len(repo_id2name)))
print("Edges: {}".format(len(user_repo_edges)))

with open("{}.user".format(sys.argv[2]), "wb") as f:
    pickle.dump(user_id2name, f)
with open("{}.repo".format(sys.argv[2]), "wb") as f:
    pickle.dump(repo_id2name, f)
with open("{}.edge".format(sys.argv[2]), "wb") as f:
    pickle.dump(user_repo_edges, f)
