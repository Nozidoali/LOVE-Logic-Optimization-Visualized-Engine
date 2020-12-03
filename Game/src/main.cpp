#include <ctime>
#include <vector>

#include "all.h"
#include "cmdline.h"

using namespace cmdline;

parser Cmdline_Parser(int argc, char * argv[])
{
    parser option;
    option.add <string> ("inputFile", 'f', "Original Circuit file", true);
    // option.add <int> ("iteration", 'i', "Iteration times", false, 1);
    // option.add <double> ("ratio", 'r', "Annealing rate", false, 0.99);
    option.add <double> ("temperature", 't', "Current temperature", false, 1);
    option.add <string> ("outputFile", 'o', "Output Circuit file", true);
    option.add <string> ("nodeName", 'n', "The name of target node", true);

    option.parse_check(argc, argv);
    return option;
}

int operationMap(string str)
{

    int result;
    if (str == "b")
        return 0;
      else if (str == "rw")
        return 1;
      else if (str == "rf")
        return 2;
      else if (str == "rs")
        return 3;
      else
        cout << "One unknown command; please input rw/rf/rs/b" << endl;
        return -1;
}



int main(int argc, char * argv[])
{

    // command line parser
    parser option = Cmdline_Parser(argc, argv);
    string filename = option.get <string> ("inputFile");
    // int n = option.get <int> ("iteration");
    // double ratio = option.get <double> ("ratio");
    // bool random = option.get <bool> ("random");
    double temp = option.get <double> ("temperature");
    string name = option.get<string> ("nodeName");
    string filename2 = option.get <string> ("outputFile");

    // double temperature = 1;

    WHY_Man * pMan = WHY_Start();
    char* Filename = (char*) filename.c_str();
    char* Filename2 = (char*) filename2.c_str();

    WHY_ReadBlif ( pMan, Filename );
//
//    cout << endl;

    WHY_PrintStats( pMan );
    cout << endl;
    SA_Rewrite (temp, pMan, name);

    WHY_WriteBlif ( pMan, Filename2 );
    cout << endl;
    WHY_Stop( pMan );
    return 0;
}
