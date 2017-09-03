import ctypes
import datetime
import pickle
import sys
import threading
import time
from ctypes import c_char_p, c_int, POINTER


# Check arguments.
if len(sys.argv) < 4:
    print("Error: missing arguments.")
    print("Usage: predict.py <shared-library> <input-starred-data> <output-predict-data>")
    sys.exit(1)

FILENAME = "/dhome/yljuang/Final/graph/star/2016/2016_bi.edgelist".encode("utf-8")
N_TOP = 100

# void octomend(int uid, int n_top, char* filename, int* ptr)
clib = ctypes.CDLL(sys.argv[1])
clib.octomend.restype = None
clib.octomend.argtypes = (c_int, c_int, c_char_p, POINTER(c_int))

with open(sys.argv[2], "rb") as f:
    all_starred = pickle.load(f)

try:
    with open(sys.argv[3], "rb") as f:
        all_predict = pickle.load(f)
except FileNotFoundError:
    print("Debug: {} not found, but created.".format(sys.argv[3]))
    all_predict = {}

def ctypes_call(uid):
    predicted_repos_array = (ctypes.c_int * N_TOP)()
    clib.octomend(c_int(int(uid)), c_int(N_TOP), c_char_p(FILENAME), predicted_repos_array)
    if all(v == 0 for v in predicted_repos_array):
        print("Warning: return NULL")
        all_predict[uid] = []
    else:
        # Convert from c array to python list.
        all_predict[uid] = [rid for rid in predicted_repos_array]

try:
    for uid in all_starred.keys():
    # for uid in [15789711]:
        print(uid)
        if uid in all_predict:
            if len(all_predict[uid]) == 0:
                print("Debug: {} is previously skipped.".format(uid))
                if uid in ["500775", "1732196", "2844591", "3759759", "4370605",
                           "4688315", "5527642", "5877145", "6257454", "6948067"]:
                    print("Debug: too many degrees.")
                    #  continue
                else:
                    print("Debug: unknown issue. Try again now.")
            else:
                print("Debug: {} already fetched.".format(uid))
                continue
        start_time = time.time()
        t = threading.Thread(target=ctypes_call, args=[uid], daemon=True)
        t.start()
        while t.is_alive():
            t.join(60.0)
        print("Elasped time: {:.0f}s ({})".format(time.time() - start_time, datetime.datetime.now()))
except KeyboardInterrupt:
    print("Debug: interrupted.")
finally:
    print("Debug: save to file {}.".format(sys.argv[3]))
    with open(sys.argv[3], "wb") as f:
        pickle.dump(all_predict, f)
