/*
 * Copyright 2017 Juang and Liang.
 * file: util.cpp
 */

#include <cmath>
#include <iostream>
#include <string>
#include <vector>

#include "util.h"

using std::cerr;
using std::endl;
using std::stoi;

bool
parse2Int(const string& line, vector<int>* tokens, char del) {
    string token;
    size_t n = myStrGetTok(line, &token, 0, del);
    while (token.size()) {
        int num = stoi(token);
        tokens->push_back(num);
        n = myStrGetTok(line, &token, n, del);
    }

    return !(tokens->size() == 0);
}

size_t
myStrGetTok(const string& str, string* tok, size_t pos, const char del) {
    size_t begin = str.find_first_not_of(del, pos);
    if (begin == string::npos) { *tok = ""; return begin; }
    size_t end = str.find_first_of(del, begin);
    *tok = str.substr(begin, end - begin);
    return end;
}

bool
myCheckArgc(const int argc, const int length, const string& usage) {
    if (argc < length) {
        cerr << "Error: missing arguments" << endl
              << "Usage: " << usage << endl;
        return false;
    }
    return true;
}

double
myLog2(const size_t x) {
    if (x <= 1)
        return 0;
    return log2(static_cast<double>(x));
}
