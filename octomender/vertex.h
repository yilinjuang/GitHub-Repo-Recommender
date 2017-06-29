/*
 * Copyright 2017 Juang and Liang.
 * file: vertex.h
 */

#ifndef OCTOMENDER_VERTEX_H_
#define OCTOMENDER_VERTEX_H_

#include <set>
#include <vector>

using std::set;
using std::vector;

class Vertex;
typedef set<Vertex*> VertexSet;
typedef vector<Vertex*> Vertices;

class Vertex {
 public:
    explicit Vertex(int id) : id_(id), score_(0.0) {}
    void add_neighbor(Vertex* v) {
        if (find(neighbors_.begin(), neighbors_.end(), v) == neighbors_.end()) {
            neighbors_.push_back(v);
        }
    }
    const Vertices& get_neighbors() const { return neighbors_; }
    size_t get_degree() const { return neighbors_.size(); }
    int get_id() const { return id_; }
    double get_score() const { return score_; }
    void inc_score(double s) { score_ += s; }
    void reset_score() { score_ = 0.0; }

 private:
    const int id_;
    double score_;
    Vertices neighbors_;
};

#endif  // OCTOMENDER_VERTEX_H_
