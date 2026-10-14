
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <algorithm>
#include <iomanip>
using namespace std;

struct Measurement {
    double t, x, y;
};

vector<Measurement> readSensor(string filename) {
    ifstream file(filename);
    vector<Measurement> data;

    if (!file.is_open()) {
        cerr << "Nie mozna otworzyc " << filename << "\n";
        return data;
    }

    string line;
    getline(file, line);

    while (getline(file, line)) {
        stringstream ss(line);
        string value;
        Measurement p;

        getline(ss, value, ',');
        p.t = stod(value);
        getline(ss, value, ',');
        p.x = stod(value);
        getline(ss, value, ',');
        p.y = stod(value);

        data.push_back(p);
    }

    sort(data.begin(), data.end(), [](const Measurement& a, const Measurement& b) {
        return a.t < b.t;
    });

    return data;
}

void correctSensor1(vector<Measurement>& data) {
    for (auto& p : data) {
        if (p.t < 17.0) {
            p.x = 0.9614 * p.x - 0.5499;
        } else {
            p.x = 0.7879 * p.x + 4.8001;
        }

        p.y = 0.9609 * p.y - 0.7352;
    }
}

void correctSensor2(vector<Measurement>& data) {
    for (auto& p : data) {
        p.y = -p.y;
    }
}

Measurement interpolate(const vector<Measurement>& data, double t) {
    if (t <= data.front().t) return data.front();
    if (t >= data.back().t) return data.back();

    int left = 0;
    int right = (int)data.size() - 1;

    while (right - left > 1) {
        int mid = (left + right) / 2;
        if (data[mid].t <= t) left = mid;
        else right = mid;
    }

    const Measurement& a = data[left];
    const Measurement& b = data[right];

    double ratio = (t - a.t) / (b.t - a.t);

    Measurement result;
    result.t = t;
    result.x = a.x + ratio * (b.x - a.x);
    result.y = a.y + ratio * (b.y - a.y);

    return result;
}

int main() {
    vector<Measurement> sensor1 = readSensor("sensor1.csv");
    vector<Measurement> sensor2 = readSensor("sensor2.csv");

    if (sensor1.empty() || sensor2.empty()) {
        cerr << "Brak danych z sensorow!\n";
        return 1;
    }

    correctSensor1(sensor1);
    correctSensor2(sensor2);

    double T;

    cout << fixed << setprecision(3);

    while (true) {
        cout << "Podaj T: ";
        if (!(cin >> T)) break;

        if (T < 0 || T > 33) {
            cout << "Wartosc spoza zakresu!\n";
            continue;
        }

        Measurement p1 = interpolate(sensor1, T);
        Measurement p2 = interpolate(sensor2, T);

        double weight1 = 0.8;
        double weight2 = 0.2;

        double x = weight1 * p1.x + weight2 * p2.x;
        double y = weight1 * p1.y + weight2 * p2.y;

        cout << x << " " << y << "\n";
    }

    return 0;
}
