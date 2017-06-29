# Octomender
```
Octomender = Octopus (GitHub) + Recommender
```
Github Repo Recommender System.

2017 Network Science Final Project with J. C. Liang.

## Requirement
- [NetworkX](https://github.com/networkx/networkx): High-productivity software for complex networks.
- [NumPy](https://github.com/numpy/numpy)
- [SciPy](https://github.com/scipy/scipy)
- [OpenMP>=4.0](http://www.openmp.org/): C/C++ API that supports multi-platform shared memory multiprocessing programming.

## Dataset
[Github Archive](https://www.githubarchive.org/)

## Preprocessing
### [parse.py](preprocessing/parse.py)
Parse raw json data files into three pickle data files.
- output-data-basename.user: map of user id (str) to user name (str)
- output-data-basename.repo: map of repo id (int) to repo name (str)
- output-data-basename.edge: list of tuples of user-repo edge (str, int)
```
Usage: parse.py {-m|--member|-w|--watch} {<input-json-directory>|<input-json-file>} <output-data-basename>
  -m, --member      parse MemberEvent.
  -w, --watch       parse WatchEvent.
Ex:    parse.py -m 2017-06-01-0.json data
Ex:    parse.py --watch json/2017-05/ data/2017-05
```
Refer raw json data format to [GitHub API v3](https://developer.github.com/v3/activity/events/types/).

### [parse_mp.py](preprocessing/parse_mp.py)
Ditto, but run with multiprocessing. Default number of processes is 16.
```
Usage: parse.py {-m|--member|-w|--watch} {<input-json-directory>|<input-json-file>} <output-data-basename> [n-process]
  -m, --member      parse MemberEvent.
  -w, --watch       parse WatchEvent.
  n-process         number of processes when multiprocessing.
Ex:    parse.py -m 2017-06-01-0.json data
Ex:    parse.py --watch json/2017-05/ data/2017-05 32
```

### [mergedata.py](preprocessing/mergedata.py)
Merge multiple pickle data files into one.
```
Usage: mergedata.py <input-data-dir> <output-data-basename>
Ex:    mergedata.py data/2016-010203/ data/2016-Q1
```

### [generate.py](preprocessing/generate.py)
Generate bipartite graph and project to unipartite graph (optional).
```
Usage: generate.py <input-data-basename> <output-graph-basename> [-p|--project]
  -p, --project     project to unipartite graph (multigraph).
Ex:    generate.py data/2017-05 graph/2017-05
Ex:    generate.py data/2016-Q1 graph/2016-Q1 -p
```
Refer implementation of bipartite graph to [algorithms.bipartite](https://networkx.readthedocs.io/en/stable/reference/algorithms.bipartite.html) of NetworkX.

### [filter.py](preprocessing/filter.py)
Filter multigraph to single graph with different mode.
```
Usage: filter.py {-m|-t|-p} <input-unipartite-nxgraph> <output-filtered-nxgraph>
  -m                filtering mode: Multiplicity > 1.
  -t                filtering mode: Top % of multiplicity.
  -p                filtering mode: Multiplicity proportion > threshold.
Ex:    filter.py -m graph/2017-05_user.nxgraph graph/2017-05_user_m.nxgraph
Ex:    filter.py -t graph/2016-Q1_repo.nxgraph graph/2016-Q1_repo_t.nxgraph
```

### [nxgraph2edgelist.py](preprocessing/nxgraph2edgelist.py)
Convert NetworkX `Graph` object (`.nxgraph`) to edge list.
```
Usage: nxgraph2edgelist.py <input-nxgraph> <output-edgelist-basename>
Ex:    nxgraph2edgelist.py graph/2017-05_bi.nxgraph graph/2017-05_bi
```

## SVD Predictor
### [bi_eval.py](svd_predictor/bi_eval.py)
### [bi_eval_sep.py](svd_predictor/bi_eval_sep.py)
### [bi_pred.py](svd_predictor/bi_pred.py)

## Octomender
### Build
```
make
```

### Run
```
Usage: ./octomender <input-edgelist>
Ex:    ./octomender graph/2017-05_bi.edgelist
```
Or direct output to file.
```
Usage: ./octomender <input-edgelist> > output.log
Ex:    ./octomender graph/2017-05_bi.edgelist > log/2017-05.log
```

### [whatsthisrepoid.py](octomender/whatsthisrepoid.py)
Convert log file to readable format including interpret repo id to repo name.
```
Usage: whatsthisrepoid.py <input-log-file> <input-repo-data-file>
Ex:    whatsthisrepoid.py log/2017-05.log data/2017-05.repo
```
