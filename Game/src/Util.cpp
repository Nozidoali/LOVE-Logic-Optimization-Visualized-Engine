#include "refactor.h"
#include "resub.h"
#include "rewrite.h"
#include "balance.h"
#include "all.h"
#include <vector>
#include <algorithm>

/**
 * Initialize the manager
 */
WHY_Man * WHY_Start ( ) {
    // initilize ABC
    Abc_Start();
    // WHY_Man * pMan = new WHY_Man;
    WHY_Man* pMan = new WHY_Man;
    return pMan;
}

/**
 * Read the network from the given file
 */
void WHY_ReadBlif ( WHY_Man * pMan, string Filename ) {

    Abc_Frame_t * pAbc = Abc_FrameGetGlobalFrame();
    ostringstream command("");
    command << "read_blif " << Filename;
    Cmd_CommandExecute( pAbc, command.str().c_str() );
    Abc_Ntk_t * pNtk = Abc_NtkDup( Abc_FrameReadNtk(pAbc) );
    pMan->pNtk = Abc_NtkStrash( pNtk, 0, 1, 0 );
    assert ( Abc_NtkIsStrash( pMan->pNtk ) );
    Abc_NtkDelete(pNtk);
    // pMan->pAig = Abc_NtkToDar( pNtk, 0, 0 );
}

/**
 * Write the rewrite network
 */
void WHY_WriteBlif ( WHY_Man * pMan, char * Filename ) {
    // if no nerwork in the pNtkNew, we check the AigNew
    Abc_Ntk_t * pNtkNetlist = Abc_NtkToNetlist( pMan->pNtk );
    Io_WriteBlif( pNtkNetlist, Filename, 0, 0, 0 );
    Abc_NtkDelete( pNtkNetlist );
}

void WHY_PrintStats ( WHY_Man * pMan ) {
    // old size / old level
    cout << Abc_NtkNodeNum( pMan->pNtk ) << "," << Abc_NtkLevel( pMan->pNtk ) << "," ;
}

/**
 * Release the memory allocated
 */
void WHY_Stop ( WHY_Man * pMan ) {
    Abc_NtkDelete( pMan->pNtk );
    // recycle memory
    Abc_Stop();
    pMan->Rfr_Gain.clear();
    pMan->Rsb_Gain.clear();
    pMan->Rwr_Gain.clear();
    delete pMan;
}



// refactor the whole network once with SA
void SA_Refactor ( double temp, WHY_Man* pMan ) {

    Abc_Ntk_t * pNtk = pMan->pNtk;
    int nNodeSizeMax = 10;
    int nConeSizeMax = 16;
    int fUpdateLevel = 1;
    int fUseZeros = 1;
    int fUseDcs = 1;
    int fVerbose = 0;


    ProgressBar * pProgress;
    Abc_ManRef_t * pManRef;
    Abc_ManCut_t * pManCut;
    Dec_Graph_t * pFForm;
    Vec_Ptr_t * vFanins;
    Abc_Obj_t * pNode;
    abctime clk, clkStart = Abc_Clock();
    int i, nNodes;

    assert( Abc_NtkIsStrash(pNtk) );
    // cleanup the AIG
    Abc_AigCleanup((Abc_Aig_t *)pNtk->pManFunc);
    // start the managers
    pManCut = Abc_NtkManCutStart( nNodeSizeMax, nConeSizeMax, 2, 1000 );
    pManRef = Abc_NtkManRefStart( nNodeSizeMax, nConeSizeMax, fUseDcs, fVerbose );
    pManRef->vLeaves   = Abc_NtkManCutReadCutLarge( pManCut );
    // compute the reverse levels if level update is requested
    if ( fUpdateLevel )
        Abc_NtkStartReverseLevels( pNtk, 0 );

    // resynthesize each node once
    pManRef->nNodesBeg = Abc_NtkNodeNum(pNtk);
    nNodes = Abc_NtkObjNumMax(pNtk);
    pProgress = Extra_ProgressBarStart( stdout, nNodes );

    // Added by MXY about random
        // random
    vector<Abc_Obj_t *> vec;
    Abc_NtkForEachNode( pNtk, pNode, i ) {
        vec.push_back( pNode );
    }

    srand( time(NULL) );

    // if (random)
    random_shuffle( vec.begin(), vec.end() );


    for ( int i=0;i<vec.size();i++ )
    {

        pNode = vec[i];

        if ( pNode == NULL ) {
            continue;
        }

        if ( pNode->Id == 0 ) {
            continue;
        }
    // end of random


    // Abc_NtkForEachNode( pNtk, pNode, i )
    // {
        Extra_ProgressBarUpdate( pProgress, i, NULL );
        // skip the constant node
//        if ( Abc_NodeIsConst(pNode) )
//            continue;
        // skip persistant nodes
        if ( Abc_NodeIsPersistant(pNode) )
            continue;
        // skip the nodes with many fanouts
        if ( Abc_ObjFanoutNum(pNode) > 1000 )
            continue;
        // stop if all nodes have been tried once
        if ( i >= nNodes )
            break;
        // compute a reconvergence-driven cut
clk = Abc_Clock();
        vFanins = Abc_NodeFindCut( pManCut, pNode, fUseDcs );
pManRef->timeCut += Abc_Clock() - clk;
        // evaluate this cut
clk = Abc_Clock();
        // pFForm = Abc_NodeRefactor( pManRef, pNode, vFanins, fUpdateLevel, fUseZeros, fUseDcs, fVerbose ); changed
        pFForm = EvalNodeRef( pManRef, pNode, vFanins);
pManRef->timeRes += Abc_Clock() - clk;
        if ( pFForm == NULL )
            continue;
//        if (pManRef->nLastGain > 0)
//         cout << pManRef->nLastGain << endl;
        // added by MXY
        if (pManRef->nLastGain < 0) {
            double threshold = exp(pManRef->nLastGain / temp);
            double rand_num = rand() / ( RAND_MAX + 1.0 );
            if (threshold <= rand_num)
                continue;
        }
        // acceptable replacement found, update the graph
clk = Abc_Clock();
        Dec_GraphUpdateNetwork( pNode, pFForm, fUpdateLevel, pManRef->nLastGain );
pManRef->timeNtk += Abc_Clock() - clk;
        Dec_GraphFree( pFForm );

        // Print result
//        WHY_PrintStats ( pMan );
//        cout << endl;
        break;
    }
    Extra_ProgressBarStop( pProgress );
pManRef->timeTotal = Abc_Clock() - clkStart;
    pManRef->nNodesEnd = Abc_NtkNodeNum(pNtk);

    // delete the managers
    Abc_NtkManCutStop( pManCut );
    Abc_NtkManRefStop( pManRef );
    // put the nodes into the DFS order and reassign their IDs
    Abc_NtkReassignIds( pNtk );
//    Abc_AigCheckFaninOrder( pNtk->pManFunc );
    // fix the levels
    if ( fUpdateLevel )
        Abc_NtkStopReverseLevels( pNtk );
    else
        Abc_NtkLevel( pNtk );
    // check
    if ( !Abc_NtkCheck( pNtk ) )
    {
        printf( "Abc_NtkRefactor: The network check has failed.\n" );
        return;
    }
    return;
}

Dec_Graph_t* EvalNodeRef(Abc_ManRef_t * p, Abc_Obj_t * pNode, Vec_Ptr_t * vFanins) {
    // Notice: (pFForm == NULL) means cannot update, check it first
    int fVeryVerbose = 0;
    int fUpdateLevel = 1;
    int fUseZeros = 1;
    int fUseDcs = 1;
    int fVerbose = 0;
    int nVars = Vec_PtrSize(vFanins);
    int nWordsMax = Abc_Truth6WordNum(p->nNodeSizeMax);
    Dec_Graph_t * pFForm;
    Abc_Obj_t * pFanin;
    word * pTruth;
    abctime clk;
    int i, nNodesSaved, nNodesAdded, Required;

    p->nNodesConsidered++;

    Required = fUpdateLevel? Abc_ObjRequiredLevel(pNode) : ABC_INFINITY;

    // get the function of the cut
clk = Abc_Clock();
    pTruth = Abc_NodeConeTruth( p->vVars, p->vFuncs, nWordsMax, pNode, vFanins, p->vVisited );
p->timeTru += Abc_Clock() - clk;
    if ( pTruth == NULL ) {
        pFForm = NULL;
        return NULL;
    }

    // always accept the case of constant node
    if ( Abc_NodeConeIsConst0(pTruth, nVars) || Abc_NodeConeIsConst1(pTruth, nVars) )
    {
        p->nLastGain = Abc_NodeMffcSize( pNode );
        p->nNodesGained += p->nLastGain;
        p->nNodesRefactored++;
        pFForm = Abc_NodeConeIsConst0(pTruth, nVars) ? Dec_GraphCreateConst0() : Dec_GraphCreateConst1();
        return Abc_NodeConeIsConst0(pTruth, nVars) ? Dec_GraphCreateConst0() : Dec_GraphCreateConst1();
    }

    // get the factored form
clk = Abc_Clock();
    pFForm = (Dec_Graph_t *)Kit_TruthToGraph( (unsigned *)pTruth, nVars, p->vMemory );
p->timeFact += Abc_Clock() - clk;

    // mark the fanin boundary
    // (can mark only essential fanins, belonging to bNodeFunc!)
    Vec_PtrForEachEntry( Abc_Obj_t *, vFanins, pFanin, i )
        pFanin->vFanouts.nSize++;
    // label MFFC with current traversal ID
    Abc_NtkIncrementTravId( pNode->pNtk );
    nNodesSaved = Abc_NodeMffcLabelAig( pNode );
    // unmark the fanin boundary and set the fanins as leaves in the form
    Vec_PtrForEachEntry( Abc_Obj_t *, vFanins, pFanin, i )
    {
        pFanin->vFanouts.nSize--;
        Dec_GraphNode(pFForm, i)->pFunc = pFanin;
    }

    // detect how many new nodes will be added (while taking into account reused nodes)
clk = Abc_Clock();
    nNodesAdded = Dec_GraphToNetworkCount( pNode, pFForm, nNodesSaved, Required );
p->timeEval += Abc_Clock() - clk;
    // quit if there is no improvement

    if ( nNodesAdded == -1 || (nNodesAdded == nNodesSaved && !fUseZeros) )
    {
        Dec_GraphFree( pFForm );
        pFForm = NULL;
        return NULL;
    }

    // compute the total gain in the number of nodes
    p->nLastGain = nNodesSaved - nNodesAdded;
    p->nNodesGained += p->nLastGain;
    p->nNodesRefactored++;

    // report the progress
    if ( fVeryVerbose )
    {
        printf( "Node %6s : ",  Abc_ObjName(pNode) );
        printf( "Cone = %2d. ", vFanins->nSize );
        printf( "FF = %2d. ",   1 + Dec_GraphNodeNum(pFForm) );
        printf( "MFFC = %2d. ", nNodesSaved );
        printf( "Add = %2d. ",  nNodesAdded );
        printf( "GAIN = %2d. ", p->nLastGain );
        printf( "\n" );
    }
    return pFForm;
}

Dec_Graph_t * Abc_NodeRefactor( Abc_ManRef_t * p, Abc_Obj_t * pNode, Vec_Ptr_t * vFanins, int fUpdateLevel, int fUseZeros, int fUseDcs, int fVerbose )
{
    int fVeryVerbose = 0;
    int nVars = Vec_PtrSize(vFanins);
    int nWordsMax = Abc_Truth6WordNum(p->nNodeSizeMax);
    Dec_Graph_t * pFForm;
    Abc_Obj_t * pFanin;
    word * pTruth;
    abctime clk;
    int i, nNodesSaved, nNodesAdded, Required;

    p->nNodesConsidered++;

    Required = fUpdateLevel? Abc_ObjRequiredLevel(pNode) : ABC_INFINITY;

    // get the function of the cut
clk = Abc_Clock();
    pTruth = Abc_NodeConeTruth( p->vVars, p->vFuncs, nWordsMax, pNode, vFanins, p->vVisited );
p->timeTru += Abc_Clock() - clk;
    if ( pTruth == NULL )
        return NULL;

    // always accept the case of constant node
    if ( Abc_NodeConeIsConst0(pTruth, nVars) || Abc_NodeConeIsConst1(pTruth, nVars) )
    {
        p->nLastGain = Abc_NodeMffcSize( pNode );
        p->nNodesGained += p->nLastGain;
        p->nNodesRefactored++;
        return Abc_NodeConeIsConst0(pTruth, nVars) ? Dec_GraphCreateConst0() : Dec_GraphCreateConst1();
    }

    // get the factored form
clk = Abc_Clock();
    pFForm = (Dec_Graph_t *)Kit_TruthToGraph( (unsigned *)pTruth, nVars, p->vMemory );
p->timeFact += Abc_Clock() - clk;

    // mark the fanin boundary
    // (can mark only essential fanins, belonging to bNodeFunc!)
    Vec_PtrForEachEntry( Abc_Obj_t *, vFanins, pFanin, i )
        pFanin->vFanouts.nSize++;
    // label MFFC with current traversal ID
    Abc_NtkIncrementTravId( pNode->pNtk );
    nNodesSaved = Abc_NodeMffcLabelAig( pNode );
    // unmark the fanin boundary and set the fanins as leaves in the form
    Vec_PtrForEachEntry( Abc_Obj_t *, vFanins, pFanin, i )
    {
        pFanin->vFanouts.nSize--;
        Dec_GraphNode(pFForm, i)->pFunc = pFanin;
    }

    // detect how many new nodes will be added (while taking into account reused nodes)
clk = Abc_Clock();
    // nNodesAdded = Dec_GraphToNetworkCount( pNode, pFForm, nNodesSaved, Required ); changed
    nNodesAdded = Dec_GraphToNetworkCount( pNode, pFForm, 100, Required );
p->timeEval += Abc_Clock() - clk;
    // quit if there is no improvement
    // cout << nNodesAdded - nNodesSaved << " "<< endl;
    // Dec_GraphFree( pFForm );
    // return NULL;
    if ( nNodesAdded == -1 || (nNodesAdded == nNodesSaved && !fUseZeros) )
    {

        Dec_GraphFree( pFForm );
        return NULL;
    }

    // compute the total gain in the number of nodes
    p->nLastGain = nNodesSaved - nNodesAdded;
    p->nNodesGained += p->nLastGain;
    p->nNodesRefactored++;

    // report the progress
    if ( fVeryVerbose )
    {
        printf( "Node %6s : ",  Abc_ObjName(pNode) );
        printf( "Cone = %2d. ", vFanins->nSize );
        printf( "FF = %2d. ",   1 + Dec_GraphNodeNum(pFForm) );
        printf( "MFFC = %2d. ", nNodesSaved );
        printf( "Add = %2d. ",  nNodesAdded );
        printf( "GAIN = %2d. ", p->nLastGain );
        printf( "\n" );
    }
    return pFForm;
}


int Dec_GraphToNetworkCount( Abc_Obj_t * pRoot, Dec_Graph_t * pGraph, int NodeMax, int LevelMax )
{
    Abc_Aig_t * pMan = (Abc_Aig_t *)pRoot->pNtk->pManFunc;
    Dec_Node_t * pNode, * pNode0, * pNode1;
    Abc_Obj_t * pAnd, * pAnd0, * pAnd1;
    int i, Counter, LevelNew, LevelOld;
    // check for constant function or a literal
    if ( Dec_GraphIsConst(pGraph) || Dec_GraphIsVar(pGraph) )
        return 0;
    // set the levels of the leaves
    Dec_GraphForEachLeaf( pGraph, pNode, i )
        pNode->Level = Abc_ObjRegular((Abc_Obj_t *)pNode->pFunc)->Level;
    // compute the AIG size after adding the internal nodes
    Counter = 0;
    Dec_GraphForEachNode( pGraph, pNode, i )
    {
        // get the children of this node
        pNode0 = Dec_GraphNode( pGraph, pNode->eEdge0.Node );
        pNode1 = Dec_GraphNode( pGraph, pNode->eEdge1.Node );
        // get the AIG nodes corresponding to the children
        pAnd0 = (Abc_Obj_t *)pNode0->pFunc;
        pAnd1 = (Abc_Obj_t *)pNode1->pFunc;
        if ( pAnd0 && pAnd1 )
        {
            // if they are both present, find the resulting node
            pAnd0 = Abc_ObjNotCond( pAnd0, pNode->eEdge0.fCompl );
            pAnd1 = Abc_ObjNotCond( pAnd1, pNode->eEdge1.fCompl );
            pAnd  = Abc_AigAndLookup( pMan, pAnd0, pAnd1 );
            // return -1 if the node is the same as the original root
            if ( Abc_ObjRegular(pAnd) == pRoot )
                return -1;
        }
        else
            pAnd = NULL;
        // count the number of added nodes
        if ( pAnd == NULL || Abc_NodeIsTravIdCurrent(Abc_ObjRegular(pAnd)) )
        {
            Counter++; //changed
            //if ( Counter > NodeMax )
            //    return -1;
        }
        // count the number of new levels
        LevelNew = 1 + Abc_MaxInt( pNode0->Level, pNode1->Level );
        if ( pAnd )
        {
            if ( Abc_ObjRegular(pAnd) == Abc_AigConst1(pRoot->pNtk) )
                LevelNew = 0;
            else if ( Abc_ObjRegular(pAnd) == Abc_ObjRegular(pAnd0) )
                LevelNew = (int)Abc_ObjRegular(pAnd0)->Level;
            else if ( Abc_ObjRegular(pAnd) == Abc_ObjRegular(pAnd1) )
                LevelNew = (int)Abc_ObjRegular(pAnd1)->Level;
            LevelOld = (int)Abc_ObjRegular(pAnd)->Level;
//            assert( LevelNew == LevelOld );
        }
        if ( LevelNew > LevelMax )
            return -1;
        pNode->pFunc = pAnd;
        pNode->Level = LevelNew;
    }
    return Counter;
}


// resub the whole network once with SA
void SA_Resub( double temp, WHY_Man* pMan )
{


    Abc_Ntk_t * pNtk = pMan->pNtk;
    int nCutMax = 8;
    int nStepsMax = 1;
    int nLevelsOdc = 0;
    int fUpdateLevel = 1;
    int fVerbose = 0;
    int fVeryVerbose = 0;


    ProgressBar * pProgress;
    Abc_ManRes_t * pManRes;
    Abc_ManCut_t * pManCut;
    Odc_Man_t * pManOdc = NULL;
    Dec_Graph_t * pFForm;
    Vec_Ptr_t * vLeaves;
    Abc_Obj_t * pNode;
    abctime clk, clkStart = Abc_Clock();
    int i, nNodes;

    assert( Abc_NtkIsStrash(pNtk) );

    // cleanup the AIG
    Abc_AigCleanup((Abc_Aig_t *)pNtk->pManFunc);
    // start the managers
    pManCut = Abc_NtkManCutStart( nCutMax, 100000, 100000, 100000 );
    pManRes = Abc_ManResubStart( nCutMax, ABC_RS_DIV1_MAX );
    if ( nLevelsOdc > 0 )
    pManOdc = Abc_NtkDontCareAlloc( nCutMax, nLevelsOdc, fVerbose, fVeryVerbose );

    // compute the reverse levels if level update is requested
    if ( fUpdateLevel )
        Abc_NtkStartReverseLevels( pNtk, 0 );

    if ( Abc_NtkLatchNum(pNtk) ) {
        Abc_NtkForEachLatch(pNtk, pNode, i)
            pNode->pNext = (Abc_Obj_t *)pNode->pData;
    }

    // resynthesize each node once
    pManRes->nNodesBeg = Abc_NtkNodeNum(pNtk);
    nNodes = Abc_NtkObjNumMax(pNtk);
    pProgress = Extra_ProgressBarStart( stdout, nNodes );


    // Added by MXY about random
    // random
    vector<Abc_Obj_t *> vec;
    Abc_NtkForEachNode( pNtk, pNode, i ) {
        vec.push_back( pNode );
    }

    srand( time(NULL) );

    random_shuffle( vec.begin(), vec.end() );


    for ( int i=0;i<vec.size();i++ )
    {

        pNode = vec[i];

        if ( pNode == NULL ) {
            continue;
        }

        if ( pNode->Id == 0 ) {
            continue;
        }
    // end of random



    // Abc_NtkForEachNode( pNtk, pNode, i )
    // {
        Extra_ProgressBarUpdate( pProgress, i, NULL );
        // skip the constant node
//        if ( Abc_NodeIsConst(pNode) )
//            continue;
        // skip persistant nodes
        if ( Abc_NodeIsPersistant(pNode) )
            continue;
        // skip the nodes with many fanouts
        if ( Abc_ObjFanoutNum(pNode) > 1000 )
            continue;
        // stop if all nodes have been tried once
        if ( i >= nNodes )
            break;

        // compute a reconvergence-driven cut
clk = Abc_Clock();
        vLeaves = Abc_NodeFindCut( pManCut, pNode, 0 );
//        vLeaves = Abc_CutFactorLarge( pNode, nCutMax );
pManRes->timeCut += Abc_Clock() - clk;
/*
        if ( fVerbose && vLeaves )
        printf( "Node %6d : Leaves = %3d. Volume = %3d.\n", pNode->Id, Vec_PtrSize(vLeaves), Abc_CutVolumeCheck(pNode, vLeaves) );
        if ( vLeaves == NULL )
            continue;
*/
        // get the don't-cares
        if ( pManOdc )
        {
clk = Abc_Clock();
            Abc_NtkDontCareClear( pManOdc );
            Abc_NtkDontCareCompute( pManOdc, pNode, vLeaves, pManRes->pCareSet );
pManRes->timeTruth += Abc_Clock() - clk;
        }

        // evaluate this cut
clk = Abc_Clock();
        pFForm = EvalNodeRes( pManRes, pNode, vLeaves );
//        Vec_PtrFree( vLeaves );
//        Abc_ManResubCleanup( pManRes );
pManRes->timeRes += Abc_Clock() - clk;
        if ( pFForm == NULL )
            continue;
        pManRes->nTotalGain += pManRes->nLastGain;

        // acceptable replacement found, update the graph
clk = Abc_Clock();

        Dec_GraphUpdateNetwork( pNode, pFForm, fUpdateLevel, pManRes->nLastGain );
pManRes->timeNtk += Abc_Clock() - clk;
        Dec_GraphFree( pFForm );

        // Print result
        // WHY_PrintStats ( pMan );
        // cout << endl;
        break;
    }
    Extra_ProgressBarStop( pProgress );
pManRes->timeTotal = Abc_Clock() - clkStart;
    pManRes->nNodesEnd = Abc_NtkNodeNum(pNtk);

    // print statistics
    if ( fVerbose )
    Abc_ManResubPrint( pManRes );

    // delete the managers
    Abc_ManResubStop( pManRes );
    Abc_NtkManCutStop( pManCut );
    if ( pManOdc ) Abc_NtkDontCareFree( pManOdc );

    // clean the data field
    Abc_NtkForEachObj( pNtk, pNode, i )
        pNode->pData = NULL;

    if ( Abc_NtkLatchNum(pNtk) ) {
        Abc_NtkForEachLatch(pNtk, pNode, i)
            pNode->pData = pNode->pNext, pNode->pNext = NULL;
    }

    // put the nodes into the DFS order and reassign their IDs
    Abc_NtkReassignIds( pNtk );
//    Abc_AigCheckFaninOrder( pNtk->pManFunc );
    // fix the levels
    if ( fUpdateLevel )
        Abc_NtkStopReverseLevels( pNtk );
    else
        Abc_NtkLevel( pNtk );
    // check
    if ( !Abc_NtkCheck( pNtk ) )
    {
        printf( "Abc_NtkRefactor: The network check has failed.\n" );
        // return 0;
        return;
    }
s_ResubTime = Abc_Clock() - clkStart;
    // return 1;
    return;
}

// With bugs here
Dec_Graph_t * EvalNodeRes( Abc_ManRes_t * p, Abc_Obj_t * pRoot, Vec_Ptr_t * vLeaves)
{

    int nSteps = 1;
    int fUpdateLevel = 1;
    int fVerbose = 0;
    Dec_Graph_t * pGraph;
    int Required;
    abctime clk;

    Required = fUpdateLevel? Abc_ObjRequiredLevel(pRoot) : ABC_INFINITY;

    assert( nSteps >= 0 );
    assert( nSteps <= 3 );
    p->pRoot = pRoot;
    p->nLeaves = Vec_PtrSize(vLeaves);
    p->nLastGain = -1;

    // collect the MFFC
clk = Abc_Clock();
    p->nMffc = Abc_NodeMffcInside( pRoot, vLeaves, p->vTemp );
p->timeMffc += Abc_Clock() - clk;
    assert( p->nMffc > 0 );

    // collect the divisor nodes
clk = Abc_Clock();
    if ( !Abc_ManResubCollectDivs( p, pRoot, vLeaves, Required ) )
        return NULL;
    p->timeDiv += Abc_Clock() - clk;

    p->nTotalDivs   += p->nDivs;
    p->nTotalLeaves += p->nLeaves;

    // simulate the nodes
clk = Abc_Clock();
    Abc_ManResubSimulate( p->vDivs, p->nLeaves, p->vSims, p->nLeavesMax, p->nWords );
p->timeSim += Abc_Clock() - clk;

clk = Abc_Clock();
    // consider constants
    if ( (pGraph = Abc_ManResubQuit( p )) )
    {
        p->nUsedNodeC++;
        p->nLastGain = p->nMffc;
        return pGraph;
    }

    // consider equal nodes
    if ( (pGraph = Abc_ManResubDivs0( p )) )
    {
p->timeRes1 += Abc_Clock() - clk;
        p->nUsedNode0++;
        p->nLastGain = p->nMffc;
        return pGraph;
    }
p->timeRes1 += Abc_Clock() - clk;
    if ( nSteps == 0 || p->nMffc == 1 )
        return NULL;

    // get the one level divisors

    Abc_ManResubDivsS( p, Required );

    // consider one node
    if ( (pGraph = Abc_ManResubDivs1( p, Required )) )
    {
p->timeRes1 += Abc_Clock() - clk;
        p->nLastGain = p->nMffc - 1;
        return pGraph;
    }
p->timeRes1 += Abc_Clock() - clk;
    if ( nSteps == 1 || p->nMffc == 2 )
        return NULL;

clk = Abc_Clock();
    // consider triples
    if ( (pGraph = Abc_ManResubDivs12( p, Required )) )
    {
p->timeRes2 += Abc_Clock() - clk;
        p->nLastGain = p->nMffc - 2;
        return pGraph;
    }
p->timeRes2 += Abc_Clock() - clk;

    // get the two level divisors
clk = Abc_Clock();
    Abc_ManResubDivsD( p, Required );
p->timeResD += Abc_Clock() - clk;

    // consider two nodes
clk = Abc_Clock();
    if ( (pGraph = Abc_ManResubDivs2( p, Required )) )
    {
p->timeRes2 += Abc_Clock() - clk;
        p->nLastGain = p->nMffc - 2;
        return pGraph;
    }
p->timeRes2 += Abc_Clock() - clk;
    if ( nSteps == 2 || p->nMffc == 3 )
        return NULL;

    // consider two nodes
clk = Abc_Clock();
    if ( (pGraph = Abc_ManResubDivs3( p, Required )) )
    {
p->timeRes3 += Abc_Clock() - clk;
        p->nLastGain = p->nMffc - 3;
        return pGraph;
    }
p->timeRes3 += Abc_Clock() - clk;
    if ( nSteps == 3 || p->nLeavesMax == 4 )
        return NULL;
    return NULL;
}


// rewrite the whole network once with SA
void SA_Rewrite( double temp, WHY_Man* pMan, string node_name )
{

    Abc_Ntk_t * pNtk = pMan->pNtk;
    int fUpdateLevel = 1;
    int fUseZeros = 1;
    int fPlaceEnable = 0;
    ProgressBar * pProgress;
    Cut_Man_t * pManCut;
    Rwr_Man_t * pManRwr;
    Abc_Obj_t * pNode;
//    Vec_Ptr_t * vAddedCells = NULL, * vUpdatedNets = NULL;
    Dec_Graph_t * pGraph;
    int i, nNodes, nGain, fCompl;
    abctime clk, clkStart = Abc_Clock();

    assert( Abc_NtkIsStrash(pNtk) );
    // cleanup the AIG
    Abc_AigCleanup((Abc_Aig_t *)pNtk->pManFunc);

    // start the rewriting manager
    pManRwr = Rwr_ManStart( 0 );
    if ( pManRwr == NULL )
        return;

    // compute the reverse levels if level update is requested
    if ( fUpdateLevel )
        Abc_NtkStartReverseLevels( pNtk, 0 );

    // start the cut manager
clk = Abc_Clock();
    pManCut = Abc_NtkStartCutManForRewrite( pNtk );
Rwr_ManAddTimeCuts( pManRwr, Abc_Clock() - clk );
    pNtk->pManCut = pManCut;

    // resynthesize each node once
    pManRwr->nNodesBeg = Abc_NtkNodeNum(pNtk);
    nNodes = Abc_NtkObjNumMax(pNtk);
    pProgress = Extra_ProgressBarStart( stdout, nNodes );

    // Added by MXY about random
    // random
    vector<Abc_Obj_t *> vec;
    Abc_NtkForEachNode( pNtk, pNode, i ) {
        vec.push_back( pNode );
    }

    srand( time(NULL) );

    random_shuffle( vec.begin(), vec.end() );


    for ( int i=0;i<vec.size();i++ )
    {

        pNode = vec[i];

        if ( pNode == NULL ) {
            continue;
        }

        if ( pNode->Id == 0 ) {
            continue;
        }
    // end of random

    // Abc_NtkForEachNode( pNtk, pNode, i )
    // {
        Extra_ProgressBarUpdate( pProgress, i, NULL );
        // stop if all nodes have been tried once
        if ( i >= nNodes )
            break;
        // skip persistant nodes
        if ( Abc_NodeIsPersistant(pNode) )
            continue;
        // skip the nodes with many fanouts
        if ( Abc_ObjFanoutNum(pNode) > 1000 )
            continue;

        // for each cut, try to resynthesize it
        nGain = EvalNodeRewrite( pManRwr, pManCut, pNode, temp, 1.0);
//        if ( !(nGain > 0 || (nGain == 0 && fUseZeros)) )
        if ( nGain == -2147483648)
            continue;
        // if we end up here, a rewriting step is accepted now we turn to the user

        // TODO: if we get here, a new structure is found

        // ! output the prompt
        cout << nGain << endl;
        cout << Abc_ObjName(pNode) << endl;
        
        // ! get the input of "1" or "0"
        int signal;
        cin >> signal;
        cerr << "signal = " << signal << endl;
        if (!signal) {
            break;
        }

        // get hold of the new subgraph to be added to the AIG
        pGraph = (Dec_Graph_t *)Rwr_ManReadDecs(pManRwr);
        fCompl = Rwr_ManReadCompl(pManRwr);

        // reset the array of the changed nodes
        if ( fPlaceEnable )
            Abc_AigUpdateReset( (Abc_Aig_t *)pNtk->pManFunc );

        // complement the FF if needed
        if ( fCompl ) Dec_GraphComplement( pGraph );
clk = Abc_Clock();
        Dec_GraphUpdateNetwork( pNode, pGraph, fUpdateLevel, nGain );
Rwr_ManAddTimeUpdate( pManRwr, Abc_Clock() - clk );
        if ( fCompl ) Dec_GraphComplement( pGraph );

        // use the array of changed nodes to update placement
//        if ( fPlaceEnable )
//            Abc_PlaceUpdate( vAddedCells, vUpdatedNets );

                // Print result
//        WHY_PrintStats ( pMan );
//        cout << endl;
        break;
    }
    Extra_ProgressBarStop( pProgress );
Rwr_ManAddTimeTotal( pManRwr, Abc_Clock() - clkStart );
    // print stats
    pManRwr->nNodesEnd = Abc_NtkNodeNum(pNtk);

    // delete the managers
    Rwr_ManStop( pManRwr );
    Cut_ManStop( pManCut );
    pNtk->pManCut = NULL;

    // start placement package
//    if ( fPlaceEnable )
//    {
//        Abc_PlaceEnd( pNtk );
//        Abc_AigUpdateStop( pNtk->pManFunc );
//    }

    // put the nodes into the DFS order and reassign their IDs
    {
//        abctime clk = Abc_Clock();
    Abc_NtkReassignIds( pNtk );
//        ABC_PRT( "time", Abc_Clock() - clk );
    }
//    Abc_AigCheckFaninOrder( pNtk->pManFunc );
    // fix the levels
    if ( fUpdateLevel )
        Abc_NtkStopReverseLevels( pNtk );
    else
        Abc_NtkLevel( pNtk );
    // check
    if ( !Abc_NtkCheck( pNtk ) )
    {
        printf( "Abc_NtkRewrite: The network check has failed.\n" );
        return;
    }
    return;
}

int EvalNodeRewrite( Rwr_Man_t * p, Cut_Man_t * pManCut, Abc_Obj_t * pNode, double temp, double ratio)
{
    int fUpdateLevel = 1;
    int fUseZeros = 1;
    int fPlaceEnable = 0;
    int fVeryVerbose = 0;
    Dec_Graph_t * pGraph;
    Cut_Cut_t * pCut;//, * pTemp;
    Abc_Obj_t * pFanin;
    unsigned uPhase;
    unsigned uTruthBest = 0; // Suppress "might be used uninitialized"
    unsigned uTruth;
    char * pPerm;
    int Required, nNodesSaved;
    int nNodesSaveCur = -1; // Suppress "might be used uninitialized"
    int i, GainCur = -1;
    // int GainBest = -1;
    int initGain = -2147483648;
    int GainBest = initGain;
    abctime clk, clk2;//, Counter;

    p->nNodesConsidered++;
    // get the required times
    Required = fUpdateLevel? Abc_ObjRequiredLevel(pNode) : ABC_INFINITY;

    // get the node's cuts
clk = Abc_Clock();
    pCut = (Cut_Cut_t *)Abc_NodeGetCutsRecursive( pManCut, pNode, 0, 0 );
    assert( pCut != NULL );
p->timeCut += Abc_Clock() - clk;


    // go through the cuts
clk = Abc_Clock();
    for ( pCut = pCut->pNext; pCut; pCut = pCut->pNext )
    {
        // consider only 4-input cuts
        if ( pCut->nLeaves < 4 )
            continue;
//            Cut_CutPrint( pCut, 0 ), printf( "\n" );

        // get the fanin permutation
        uTruth = 0xFFFF & *Cut_CutReadTruth(pCut);
        pPerm = p->pPerms4[ (int)p->pPerms[uTruth] ];
        uPhase = p->pPhases[uTruth];
        // collect fanins with the corresponding permutation/phase
        Vec_PtrClear( p->vFaninsCur );
        Vec_PtrFill( p->vFaninsCur, (int)pCut->nLeaves, 0 );
        for ( i = 0; i < (int)pCut->nLeaves; i++ )
        {
            pFanin = Abc_NtkObj( pNode->pNtk, pCut->pLeaves[(int)pPerm[i]] );
            if ( pFanin == NULL )
                break;
            pFanin = Abc_ObjNotCond(pFanin, ((uPhase & (1<<i)) > 0) );
            Vec_PtrWriteEntry( p->vFaninsCur, i, pFanin );
        }
        if ( i != (int)pCut->nLeaves )
        {
            p->nCutsBad++;
            continue;
        }
        p->nCutsGood++;

        {
            int Counter = 0;
            Vec_PtrForEachEntry( Abc_Obj_t *, p->vFaninsCur, pFanin, i )
                if ( Abc_ObjFanoutNum(Abc_ObjRegular(pFanin)) == 1 )
                    Counter++;
            if ( Counter > 2 )
                continue;
        }

clk2 = Abc_Clock();

        // mark the fanin boundary
        Vec_PtrForEachEntry( Abc_Obj_t *, p->vFaninsCur, pFanin, i )
            Abc_ObjRegular(pFanin)->vFanouts.nSize++;

        // label MFFC with current ID
        Abc_NtkIncrementTravId( pNode->pNtk );
        nNodesSaved = Abc_NodeMffcLabelAig( pNode );
        // unmark the fanin boundary
        Vec_PtrForEachEntry( Abc_Obj_t *, p->vFaninsCur, pFanin, i )
            Abc_ObjRegular(pFanin)->vFanouts.nSize--;
p->timeMffc += Abc_Clock() - clk2;

        // evaluate the cut
clk2 = Abc_Clock();
        pGraph = Rwr_CutEvaluate( p, pNode, pCut, p->vFaninsCur, nNodesSaved, Required, &GainCur, fPlaceEnable );
p->timeEval += Abc_Clock() - clk2;

        // check if the cut is better than the current best one
        if ( pGraph != NULL && GainBest < GainCur )
        {
            // save this form
            nNodesSaveCur = nNodesSaved;
            GainBest  = GainCur;
            p->pGraph  = pGraph;
            p->fCompl = ((uPhase & (1<<4)) > 0);
            uTruthBest = 0xFFFF & *Cut_CutReadTruth(pCut);
            // collect fanins in the
            Vec_PtrClear( p->vFanins );
            Vec_PtrForEachEntry( Abc_Obj_t *, p->vFaninsCur, pFanin, i )
                Vec_PtrPush( p->vFanins, pFanin );
        }
    }
p->timeRes += Abc_Clock() - clk;

//    if ( GainBest == -1 )
//        return -1;
      if ( GainBest == initGain )
        return initGain;

     // added by MXY
    if (GainBest < 0) {
            double threshold = exp(GainBest / temp);
            double rand_num = rand() / ( RAND_MAX + 1.0 );
            if (threshold <= rand_num)
                return initGain;
    }
    // temp *= ratio;



    // copy the leaves
    Vec_PtrForEachEntry( Abc_Obj_t *, p->vFanins, pFanin, i )
        Dec_GraphNode((Dec_Graph_t *)p->pGraph, i)->pFunc = pFanin;
/*
    printf( "(" );
    Vec_PtrForEachEntry( Abc_Obj_t *, p->vFanins, pFanin, i )
        printf( " %d", Abc_ObjRegular(pFanin)->vFanouts.nSize - 1 );
    printf( " )  " );
*/
//    printf( "%d ", Rwr_NodeGetDepth_rec( pNode, p->vFanins ) );

    p->nScores[p->pMap[uTruthBest]]++;
    p->nNodesGained += GainBest;
    if ( fUseZeros || GainBest > 0 )
    {
        p->nNodesRewritten++;
    }

    // report the progress
    if ( fVeryVerbose && GainBest > 0 )
    {
        printf( "Node %6s :   ", Abc_ObjName(pNode) );
        printf( "Fanins = %d. ", p->vFanins->nSize );
        printf( "Save = %d.  ", nNodesSaveCur );
        printf( "Add = %d.  ",  nNodesSaveCur-GainBest );
        printf( "GAIN = %d.  ", GainBest );
        printf( "Cone = %d.  ", p->pGraph? Dec_GraphNodeNum((Dec_Graph_t *)p->pGraph) : 0 );
        printf( "Class = %d.  ", p->pMap[uTruthBest] );
        printf( "\n" );
    }
    return GainBest;
}


Dec_Graph_t * Rwr_CutEvaluate( Rwr_Man_t * p, Abc_Obj_t * pRoot, Cut_Cut_t * pCut, Vec_Ptr_t * vFaninsCur, int nNodesSaved, int LevelMax, int * pGainBest, int fPlaceEnable )
{
    Vec_Ptr_t * vSubgraphs;
    Dec_Graph_t * pGraphBest = NULL; // Suppress "might be used uninitialized"
    Dec_Graph_t * pGraphCur;
    Rwr_Node_t * pNode, * pFanin;
    int nNodesAdded, GainBest, i, k;
    unsigned uTruth;
    float CostBest;//, CostCur;
    // find the matching class of subgraphs
    uTruth = 0xFFFF & *Cut_CutReadTruth(pCut);
    vSubgraphs = Vec_VecEntry( p->vClasses, p->pMap[uTruth] );
    p->nSubgraphs += vSubgraphs->nSize;
    // determine the best subgraph
    int initGain = -2147483648;
    GainBest = initGain;
    // GainBest = -1;
    CostBest = ABC_INFINITY;
    Vec_PtrForEachEntry( Rwr_Node_t *, vSubgraphs, pNode, i )
    {
        // get the current graph
        pGraphCur = (Dec_Graph_t *)pNode->pNext;
        // copy the leaves
        Vec_PtrForEachEntry( Rwr_Node_t *, vFaninsCur, pFanin, k )
            Dec_GraphNode(pGraphCur, k)->pFunc = pFanin;
        // detect how many unlabeled nodes will be reused
        nNodesAdded = Dec_GraphToNetworkCount( pRoot, pGraphCur, nNodesSaved, LevelMax );
        if ( nNodesAdded == -1 )
            continue;
        // assert( nNodesSaved >= nNodesAdded );

        {
            // count the gain at this node
            if ( GainBest < nNodesSaved - nNodesAdded )
            {
                GainBest   = nNodesSaved - nNodesAdded;
                pGraphBest = pGraphCur;

                // score the graph
                if ( nNodesSaved - nNodesAdded > 0 )
                {
                    pNode->nScore++;
                    pNode->nGain += GainBest;
                    pNode->nAdded += nNodesAdded;
                }
            }
        }
    }
    // if ( GainBest == -1 )
    if (GainBest == initGain)
        return NULL;
    *pGainBest = GainBest;
    return pGraphBest;
}


void SA_Balance ( double temp, WHY_Man* pMan ) {
    Abc_NtkBalance  ( pMan->pNtk, 0, 0, 1 );
}

