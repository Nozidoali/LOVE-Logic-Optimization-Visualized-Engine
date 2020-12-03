#ifndef RESUB_H
#define RESUB_H

#include <cstdlib>
#include <iostream>
#include <algorithm>
#include <cstring>
#include <fstream>
#include <vector>
#include <sstream>
#include <queue>
#include <map>
#include "abcApi.h"
#include "all.h"


using namespace std;
// balance
extern Abc_Ntk_t* Abc_NtkBalance  ( Abc_Ntk_t * pNtk, int fDuplicate, int fSelective, int fUpdateLevel );



#endif
