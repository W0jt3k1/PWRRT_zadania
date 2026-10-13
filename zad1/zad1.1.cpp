#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <map>
#include <algorithm>
#include <iomanip>

using namespace std;

struct Cone {
    int id;
    double x, y;
};

bool cmp(const Cone& A, const Cone& B, double m) {
    double dx = A.x - B.x;
    double dy = A.y - B.y;
    return dx * dx + dy * dy <= m * m;
}

int find(int x, vector<int>& parent) {
    if (parent[x] != x) {
        parent[x] = find(parent[x], parent);
    }
    return parent[x];
}

void unite(int a, int b, vector<int>& parent) {
    int rootA = find(a, parent);
    int rootB = find(b, parent);

    if (rootA != rootB) {
        parent[rootB] = rootA;
    }
}

int main() {
    ifstream file("example_input.txt");
    if (!file.is_open()) {
        cerr << "Nie mozna otworzyc pliku!\n";
        return 1;
    }
    cout << fixed << setprecision(3);
    int n;
    double m;

    file >> n >> m;

    vector<Cone> cones;
    for(int i =0; i<n; i++){
        Cone cone;
        file >> cone.id >> cone.x >> cone.y;
        cones.push_back(cone);
    }

    vector<int> parent(n);

    for (int i = 0; i < n; i++) {
        parent[i] = i;
    }

    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (cmp(cones[i], cones[j], m)) {
                unite(i, j, parent);
            }
        }
    }
    map<int, vector<int>> groups;

    for (int i = 0; i < n; i++) {
        groups[find(i, parent)].push_back(i);
    } 
    int nextId = 0;

for (const Cone& cone : cones) {
    nextId = max(nextId, cone.id);
}
nextId++;

vector<Cone> newCones;

for (const auto& [root, indices] : groups) {
    if (indices.size() == 1) {
        newCones.push_back(cones[indices[0]]);
        continue;
    }

    double sumX = 0, sumY = 0;

    for (int i : indices) {
        sumX += cones[i].x;
        sumY += cones[i].y;
    }

    Cone merged;
    merged.id = nextId++;
    merged.x = sumX / indices.size();
    merged.y = sumY / indices.size();

    newCones.push_back(merged);

    cout << "CONE " << merged.id << " "<< merged.x << " " << merged.y << " [";

    for (int i = 0; i < indices.size(); i++) {
        if (i > 0) cout << ",";
        cout << cones[indices[i]].id;
    }

    cout << "]\n";
}
    return 0;
}