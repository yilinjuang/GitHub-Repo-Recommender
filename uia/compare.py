""" Compare real starred records with predicted ones based on real data in 2016

"""
import datetime
import pickle
import sys


# Check arguments.
if len(sys.argv) < 3:
    print("Error: missing arguments.")
    print("Usage: predict.py <input-starred-data> <input-predict-data>")
    sys.exit(1)

print("Loading starred")
with open(sys.argv[1], "rb") as f:
    ALL_STAR = pickle.load(f)

print("Loading predict")
with open(sys.argv[2], "rb") as f:
    ALL_PREDICT = pickle.load(f)

print("Comparing")
for uid in ALL_PREDICT.keys():
    if len(ALL_PREDICT[uid]) == 0:
        continue

    print("UID: {}".format(uid))
    rid_2017 = []  # 2017
    rid_2016 = []  # 2016
    rid_past = []  # ~2015

    for star in ALL_STAR[uid]:
        rid = star['repo']['id']
        timestamp = datetime.datetime.strptime(star['starred_at'],
                                               "%Y-%m-%dT%H:%M:%SZ")
        if timestamp.year == 2017:
            rid_2017.append(rid)
        elif timestamp.year == 2016:
            rid_2016.append(rid)
        else:
            rid_past.append(rid)

    hit_2017 = 0
    hit_2016 = 0
    hit_past = 0
    miss = 0
    for predict_rid in ALL_PREDICT[uid]:
        if predict_rid in rid_2017:
            hit_2017 += 1
        elif predict_rid in rid_2016:
            hit_2016 += 1
        elif predict_rid in rid_past:
            hit_past += 1
        else:
            miss += 1

    n_predict = len(ALL_PREDICT[uid])
    assert n_predict == hit_2017 + hit_2016 + hit_past + miss
    # assert hit_2016 == 0
    print("Hit 2017:  {:> 6.2f}% ({:>3}/{})".format(hit_2017/n_predict*100,
                                                    hit_2017, n_predict))
    print("Hit 2016:  {:> 6.2f}% ({:>3}/{})".format(hit_2016/n_predict*100,
                                                    hit_2016, n_predict))
    print("Hit ~2015: {:> 6.2f}% ({:>3}/{})".format(hit_past/n_predict*100,
                                                    hit_past, n_predict))
    print("Hit all:   {:> 6.2f}% ({:>3}/{})".format((hit_2017+hit_past)/n_predict*100,
                                                    (hit_2017+hit_past), n_predict))
