/*************************************
	repo:	Desktop/myfile
	file:	myUtil.cpp
	mod.:	20170529
*************************************/

#include <cmath>
#include <iostream>
#include <string>
#include <vector>

#include "myUtil.h"

using std::cerr;
using std::endl;

int
str2Int(const string& str) {
   int num = 0, sign = 1;
   for(size_t i = 0; i < str.size(); i++) {
      if(i == 0 && str[0] == '-') sign = -1;
      else if(isdigit(str[i])) { num *= 10; num += int(str[i] - '0'); }
   }

   return num * sign;
}

bool str2Int(const string& str, int& num) {
   num = 0;
   int sign = 1;
   for(size_t i = 0; i < str.size(); i++) {
      if(i == 0 && str[0] == '-') sign = -1;
      else if(isdigit(str[i])) { num *= 10; num += int(str[i] - '0'); }
      else return false;
   }

   num *= sign;
   return true;
}

float
str2Float(const string &str) {
   float num = 0, sign = 1;
   size_t j = str.size();
   for(size_t i = 0; i < str.size(); i++) {
      if(i == 0 && str[0] == '-') sign = -1;
      else if(isdigit(str[i])) { num *= 10; num += float(str[i] - '0'); }
      else if(str[i] == '.') j = i;
   }

   for(size_t i = str.size() - 1; i > j; i--) num /= 10;

   return num * sign;
}

bool
str2Float(const string& str, float& num) {
   num = 0;
   float sign = 1;
   size_t j = str.size();
   for(size_t i = 0; i < str.size(); i++) {
      if(i == 0 && str[0] == '-') sign = -1;
      else if(isdigit(str[i])) { num *= 10; num += float(str[i] - '0'); }
      else if(str[i] == '.' && j == str.size()) j = i;
      else return false;
   }

   for(size_t i = str.size() - 1; i > j; i--) num /= 10;

   num *= sign;
   return true;
}

bool
parse2Int(const string& line, vector<int>& tokens, char del) {
   string token;
   size_t n = myStrGetTok(line, token, 0, del);
   while(token.size()) {
      int num = str2Int(token);
      tokens.push_back(num);
      n = myStrGetTok(line, token, n, del);
   }

   return !(tokens.size() == 0);
}

size_t
myStrGetTok(const string& str, string& tok, size_t pos, const char del) {
   size_t begin = str.find_first_not_of(del, pos);
   if(begin == string::npos) { tok = ""; return begin; }
   size_t end = str.find_first_of(del, begin);
   tok = str.substr(begin, end - begin);
   return end;
}

bool
myCheckArgc(const int argc, const int length, const string& usage) {
   if(argc < length) {
      cerr << "Error: not enough parameter(s)!!\n"
           << "Usage: " << usage << endl;
      return false;
   }

   return true;
}

/*
bool
myOpenFile(char *argv, ifstream& ifile) {
   ifile.open(argv, ios::in);
   if(!ifile.is_open()) {
      cerr << "Error: File \'" << argv << "\' failed to open!!" << endl;
      return false;
   }

   return true;
}*/

double
myLog2(const size_t x) {
   if(x <= 1) return 0;
   else return log2(double(x));
}
