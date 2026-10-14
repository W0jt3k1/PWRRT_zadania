import csv
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

folder = Path(__file__).resolve().parent


def read_sensor(filename):
    t, x, y = [], [], []
    with open(folder / filename) as file:
        for row in csv.DictReader(file):
            t.append(float(row["timestamp"]))
            x.append(float(row["x"]))
            y.append(float(row["y"]))
    return np.array(t), np.array(x), np.array(y)


t1, x1, y1 = read_sensor("sensor1.csv")
t2, x2, y2 = read_sensor("sensor2.csv")

# Korekta osi Y sensora 2
y2_corrected = -y2

# Oszacowanie przesuniecia X sensora 1
change_time = 17.0
x2_interp = np.interp(t1, t2, x2)
difference = x2_interp - x1

before = (t1 >= 4) & (t1 < 16)
after = (t1 >= 18) & (t1 <= 32)

offset_before = np.median(difference[before])
offset_after = np.median(difference[after])
offset = offset_after - offset_before

x1_corrected = x1.copy()
x1_corrected[t1 >= change_time] += offset

print(f"Przesuniecie X po 17 s: {offset:.3f} m")

# Wzorcowa geometria skidpada
radius = 18.25 / 2
angle = np.linspace(0, 2 * np.pi, 300)

# Srodki okregow wzgledem osi Y
left_y = radius
right_y = -radius

circle_x = radius * np.cos(angle)
left_circle_y = left_y + radius * np.sin(angle)
right_circle_y = right_y + radius * np.sin(angle)

fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# Oryginalne trajektorie
axes[0, 0].plot(x1, y1, label="Sensor 1")
axes[0, 0].plot(x2, y2, label="Sensor 2")
axes[0, 0].set_title("Oryginalna trajektoria XY")

# Trajektorie po korekcie
axes[0, 1].plot(x1_corrected, y1, label="Sensor 1")
axes[0, 1].plot(x2, y2_corrected, label="Sensor 2")
axes[0, 1].set_title("Trajektoria po korekcie")

# Trajektorie i wzorcowy skidpad
axes[0, 2].plot(x1_corrected, y1, label="Sensor 1")
axes[0, 2].plot(x2, y2_corrected, label="Sensor 2")
axes[0, 2].plot(circle_x, left_circle_y, "k--", label="Wzorcowy tor")
axes[0, 2].plot(circle_x, right_circle_y, "k--")
axes[0, 2].set_title("Porownanie z geometria toru")

# X przed i po korekcie
axes[1, 0].plot(t1, x1, label="Sensor 1")
axes[1, 0].plot(t2, x2, label="Sensor 2")
axes[1, 0].set_title("X przed korekta")
axes[1, 0].set_xlabel("Czas [s]")

axes[1, 1].plot(t1, x1_corrected, label="Sensor 1")
axes[1, 1].plot(t2, x2, label="Sensor 2")
axes[1, 1].set_title("X po korekcie")
axes[1, 1].set_xlabel("Czas [s]")

# Y po odwroceniu znaku
axes[1, 2].plot(t1, y1, label="Sensor 1")
axes[1, 2].plot(t2, y2_corrected, label="Sensor 2")
axes[1, 2].set_title("Y po korekcie")
axes[1, 2].set_xlabel("Czas [s]")

for ax in axes.flat:
    ax.grid(True)
    ax.legend()
    if ax in axes[0]:
        ax.set_aspect("equal")
        ax.set_xlabel("X [m]")
        ax.set_ylabel("Y [m]")
    else:
        ax.set_ylabel("Pozycja [m]")

plt.tight_layout()
plt.savefig(folder / "visualisation2.png", dpi=200)
