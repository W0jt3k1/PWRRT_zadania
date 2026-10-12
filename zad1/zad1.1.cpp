#include <iostream>
#include <fstream>
#include <vector>
using namespace std;

int main() {
    ifstream file('example_input.txt');
    if (!file.is_open()) {
        cerr << "Nie mozna otworzyc pliku!\n";
        return 1;
    }

    int n;
    double m;

    file >> n >> m;
    return 0;
}