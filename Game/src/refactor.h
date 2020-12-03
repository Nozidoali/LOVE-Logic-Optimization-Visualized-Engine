#ifndef REFACTOR_H
#define REFACTOR_H

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

// refactor
struct Abc_ManRef_t_
{
    // user specified parameters
    int              nNodeSizeMax;      // the limit on the size of the supernode
    int              nConeSizeMax;      // the limit on the size of the containing cone
    int              fVerbose;          // the verbosity flag
    // internal data structures
    Vec_Ptr_t *      vVars;             // truth tables
    Vec_Ptr_t *      vFuncs;            // functions
    Vec_Int_t *      vMemory;           // memory
    Vec_Str_t *      vCube;             // temporary
    Vec_Int_t *      vForm;             // temporary
    Vec_Ptr_t *      vVisited;          // temporary
    Vec_Ptr_t *      vLeaves;           // temporary
    // node statistics
    int              nLastGain;
    int              nNodesConsidered;
    int              nNodesRefactored;
    int              nNodesGained;
    int              nNodesBeg;
    int              nNodesEnd;
    // runtime statistics
    abctime          timeCut;
    abctime          timeTru;
    abctime          timeDcs;
    abctime          timeSop;
    abctime          timeFact;
    abctime          timeEval;
    abctime          timeRes;
    abctime          timeNtk;
    abctime          timeTotal;
};

typedef struct Abc_ManRef_t_   Abc_ManRef_t;

// ABC functions
extern "C" int Abc_NtkRefactor( Abc_Ntk_t * pNtk, int nNodeSizeMax, int nConeSizeMax, int fUpdateLevel, int fUseZeros, int fUseDcs, int fVerbose );
extern "C" Abc_ManRef_t * Abc_NtkManRefStart( int nNodeSizeMax, int nConeSizeMax, int fUseDcs, int fVerbose );
extern "C" void Abc_NtkManRefStop( Abc_ManRef_t * p );
extern "C" int Abc_NodeConeIsConst0( word * pTruth, int nVars );
extern "C" int Abc_NodeConeIsConst1( word * pTruth, int nVars );
extern "C" word * Abc_NodeConeTruth( Vec_Ptr_t * vVars, Vec_Ptr_t * vFuncs, int nWordsMax, Abc_Obj_t * pRoot, Vec_Ptr_t * vLeaves, Vec_Ptr_t * vVisited );
// extern "C" void Dec_GraphUpdateNetwork( Abc_Obj_t * pRoot, Dec_Graph_t * pGraph, int fUpdateLevel, int nGain );
Dec_Graph_t * Abc_NodeRefactor( Abc_ManRef_t * p, Abc_Obj_t * pNode, Vec_Ptr_t * vFanins, int fUpdateLevel, int fUseZeros, int fUseDcs, int fVerbose );



// My own functions
Dec_Graph_t * EvalNodeRef(Abc_ManRef_t * p, Abc_Obj_t * pNode, Vec_Ptr_t * vFanins);

#endif
