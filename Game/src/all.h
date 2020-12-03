#ifndef ALL_H
#define ALL_H

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
#include <bits/stdc++.h>
//#include <boost/algorithm/string.hpp>
//#include <string>

using namespace std;


struct WHY_Man {

    Abc_Ntk_t * pNtk;
    map<unsigned int, int> Rwr_Gain;
    map<unsigned int, int> Rfr_Gain;
    map<unsigned int, int> Rsb_Gain;
    map<unsigned int, int> Rwr_Waste;
    map<unsigned int, int> Rfr_Waste;
    map<unsigned int, int> Rsb_Waste;


};

// common functions
extern "C" void Dec_GraphUpdateNetwork( Abc_Obj_t * pRoot, Dec_Graph_t * pGraph, int fUpdateLevel, int nGain );
int Dec_GraphToNetworkCount( Abc_Obj_t * pRoot, Dec_Graph_t * pGraph, int NodeMax, int LevelMax );


/* Util.cpp */
WHY_Man * WHY_Start ();
void WHY_ReadBlif ( WHY_Man * pMan, string Filename );
void WHY_WriteBlif ( WHY_Man * pMan, char * Filename );
void WHY_PrintStats ( WHY_Man * pMan );
void WHY_Stop ( WHY_Man * pMan ) ;

void SA_Refactor (double temp,  WHY_Man* pMan);
void SA_Resub (double temp,  WHY_Man* pMan );
void SA_Rewrite( double temp,  WHY_Man* pMan, string node_name );
void SA_Balance( double temp,  WHY_Man* pMan );
#endif
