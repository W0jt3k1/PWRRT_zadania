
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <iomanip>
using namespace std;

struct Cone {
    int id;
    double x, y;
};

double cross(const Cone& A, const Cone& B, const Cone& C) {
    return (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x);
}

double dist(const Cone& A, const Cone& B) {
    double dx = A.x - B.x;
    double dy = A.y - B.y;
    return sqrt(dx * dx + dy * dy);
}

vector<Cone> convexHull(vector<Cone> cones) {
    if (cones.size() <= 1) return cones;

    sort(cones.begin(), cones.end(), [](const Cone& A, const Cone& B) {
        if (A.x != B.x) return A.x < B.x;
        return A.y < B.y;
    });

    vector<Cone> lower, upper;

    for (const Cone& p : cones) {
        while (lower.size() >= 2 && cross(lower[lower.size() - 2], lower.back(), p) <= 0) {
            lower.pop_back();
        }
        lower.push_back(p);
    }

    for (int i = (int)cones.size() - 1; i >= 0; i--) {
        const Cone& p = cones[i];
        while (upper.size() >= 2 && cross(upper[upper.size() - 2], upper.back(), p) <= 0) {
            upper.pop_back();
        }
        upper.push_back(p);
    }

    lower.pop_back();
    upper.pop_back();
    lower.insert(lower.end(), upper.begin(), upper.end());

    return lower;
}

double perimeter(const vector<Cone>& hull) {
    double result = 0;
    if (hull.size() <= 1) return 0;

    for (int i = 0; i < (int)hull.size(); i++) {
        result += dist(hull[i], hull[(i + 1) % hull.size()]);
    }
    return result;
}

int main() {
    ifstream file("example_input.txt");
    if (!file.is_open()) {
        cerr << "Nie mozna otworzyc pliku!\n";
        return 1;
    }

    int n;
    double m;
    file >> n >> m;

    vector<Cone> cones;
    for (int i = 0; i < n; i++) {
        Cone cone;
        file >> cone.id >> cone.x >> cone.y;
        cones.push_back(cone);
    }

    vector<Cone> hull = convexHull(cones);

    cout << fixed << setprecision(3);
    cout << "ENCLOSURE " << perimeter(hull) << " [";

    for (int i = 0; i < (int)hull.size(); i++) {
        if (i > 0) cout << ",";
        cout << hull[i].id;
    }
    cout << "]\n";

    return 0;
}
