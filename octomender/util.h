/*
 * Copyright 2017 Juang and Liang.
 * file: util.h
 */

#ifndef OCTOMENDER_UTIL_H_
#define OCTOMENDER_UTIL_H_

#include <string>
#include <vector>

using std::string;
using std::vector;

bool parse2Int(const string& line, vector<int>* tokens, char del);
size_t myStrGetTok(const string& str, string* tok, size_t pos, const char del);

bool myCheckArgc(const int argc, const int length, const string& usage);
double myLog2(const size_t x);

#endif  // OCTOMENDER_UTIL_H_
