import pickle
import sys


# Check arguments.
if len(sys.argv) < 3:
    print("Error: missing arguments.")
    print("Usage: lookup.py <input-data-file> <query>")
    sys.exit(1)
if not sys.argv[1].endswith((".user", ".repo")):
    print("Error: invalid data file {}.".format(sys.argv[1]))
    sys.exit(1)

with open(sys.argv[1], "rb") as f:
    dictionary = pickle.load(f)

result = None
try:
    # query is id.
    id_ = int(sys.argv[2])
    try:
        if sys.argv[1].endswith(".user"):
            result = dictionary[str(id_)]
        elif sys.argv[1].endswith(".repo"):
            result = dictionary[id_]
    except KeyError:
        pass
except ValueError:
    # query is name.
    for k, v in dictionary.items():
        if v == sys.argv[2]:
            result = k
            break

if result:
    print("{} -> {}".format(sys.argv[2], result))
else:
    print("Warning: query {} not found.".format(sys.argv[2]))
