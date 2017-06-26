/*************************************
	repo:	Desktop/myfile
	file:	myUtil.h
	mod.:	20170516
*************************************/

#ifndef MYUTIL_H
#define MYUTIL_H

#include <fstream>
#include <vector>
#include <string>

using std::string;
using std::vector;

int str2Int(const string& str);
bool str2Int(const string& str, int& num);
float str2Float(const string& str);
bool str2Float(const string& str, float& num);

bool parse2Int(const string& line, vector<int>& tokens, char del);
size_t myStrGetTok(const string& str, string& tok, size_t pos, const char del);

bool myCheckArgc(const int argc, const int length, const string& usage);
// bool myOpenFile(char *argv, ifstream& ifile);
double myLog2(const size_t x);

#endif
