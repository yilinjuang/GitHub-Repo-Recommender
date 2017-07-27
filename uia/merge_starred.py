import os
import pickle
import sys


# Check arguments.
if len(sys.argv) < 2:
    print("Error: missing arguments.")
    print("Usage: merge_starred.py <starred-data-basename>")
    sys.exit(1)

all_starred = {}
for file in os.listdir("."):
    if file.startswith(sys.argv[1]):
        print(file, end="")
        with open(file, "rb") as f:
            starred = pickle.load(f)
            # print(starred.keys())
            all_starred = {**all_starred, **starred}

with open(sys.argv[1], "wb") as f:
    pickle.dump(all_starred, f)
