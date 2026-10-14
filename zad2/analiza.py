import csv
import numpy as np
from pathlib import Path

folder = Path(__file__).resolve().parent


def read_sensor(filename):
    data = []
    with open(folder / filename) as file:
        for row in csv.DictReader(file):
            data.append([float(row["timestamp"]), float(row["x"]), float(row["y"])])
    return np.array(data)


def fit(a, b):
    scale, offset = np.polyfit(a, b, 1)
    return scale, offset


def noise(values):
    # Porownanie punktu z interpolacja miedzy sasiadami
    predicted = (values[:-2] + values[2:]) / 2
    errors = values[1:-1] - predicted
    return np.std(errors), np.max(np.abs(errors))


s1 = read_sensor("sensor1.csv")
s2 = read_sensor("sensor2.csv")

t1, x1, y1 = s1.T
t2, x2, y2 = s2.T

# Sensor 2 ma odwrocona os Y
y2 = -y2

# Synchronizacja czasowa
x1i = np.interp(t2, t1, x1)
y1i = np.interp(t2, t1, y1)

before = (t2 >= 4) & (t2 < 16)
after = (t2 >= 18) & (t2 <= 32)

print("CZESTOTLIWOSC")
for name, t in [("Sensor 1", t1), ("Sensor 2", t2)]:
    print(f"{name}: {len(t)} pomiarow, {1 / np.mean(np.diff(t)):.2f} Hz")

print("\nSKALA I PRZESUNIECIE")
for name, a, b, mask in [
    ("X przed 17 s", x1i, x2, before),
    ("X po 17 s", x1i, x2, after),
    ("Y", y1i, y2, np.ones(len(t2), dtype=bool)),
]:
    scale, offset = fit(a[mask], b[mask])
    print(f"{name}: skala = {scale:.4f}, offset = {offset:.4f} m")

print("\nROZNICA X")
difference = x2 - x1i
print(f"Przed 17 s: {np.median(difference[before]):.3f} m")
print(f"Po 17 s: {np.median(difference[after]):.3f} m")

print("\nLOKALNE ODCHYLENIA")
for name, values in [
    ("Sensor 1 X", x1),
    ("Sensor 1 Y", y1),
    ("Sensor 2 X", x2),
    ("Sensor 2 Y", y2),
]:
    std, maximum = noise(values)
    print(f"{name}: std = {std:.4f} m, max = {maximum:.4f} m")
