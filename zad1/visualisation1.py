import matplotlib.pyplot as plt


def read_cones(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    n = int(lines[0].strip())
    m = float(lines[1].strip())

    cones = []
    for line in lines[2 : 2 + n]:
        parts = line.strip().split()
        cone_id = int(parts[0])
        x = float(parts[1])
        y = float(parts[2])
        cones.append((cone_id, x, y))

    return m, cones


def cross(a, b, c):
    return (b[1] - a[1]) * (c[2] - a[2]) - (b[2] - a[2]) * (c[1] - a[1])


def convex_hull(cones):
    if len(cones) <= 1:
        return cones

    cones = sorted(cones, key=lambda p: (p[1], p[2]))

    lower = []
    for p in cones:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(cones):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]


def plot_input(ax, cones):
    xs = [c[1] for c in cones]
    ys = [c[2] for c in cones]

    ax.scatter(xs, ys)
    for cone_id, x, y in cones:
        ax.text(x + 0.1, y + 0.1, str(cone_id), fontsize=9)

    ax.set_title("Input")
    ax.set_aspect("equal")
    ax.grid(True)


def plot_dedup(ax, original, dedup):
    original_ids = {c[0] for c in original}

    old_cones = []
    new_cones = []

    for cone in dedup:
        if cone[0] in original_ids:
            old_cones.append(cone)
        else:
            new_cones.append(cone)

    if old_cones:
        xs = [c[1] for c in old_cones]
        ys = [c[2] for c in old_cones]
        ax.scatter(xs, ys, label="stare")

        for cone_id, x, y in old_cones:
            ax.text(x + 0.1, y + 0.1, str(cone_id), fontsize=9)

    if new_cones:
        xs = [c[1] for c in new_cones]
        ys = [c[2] for c in new_cones]
        ax.scatter(xs, ys, marker="x", s=100, label="dodane")

        for cone_id, x, y in new_cones:
            ax.text(x + 0.1, y + 0.1, str(cone_id), fontsize=9)

    ax.set_title("Po deduplikacji")
    ax.set_aspect("equal")
    ax.grid(True)
    ax.legend()


def plot_hull(ax, dedup):
    xs = [c[1] for c in dedup]
    ys = [c[2] for c in dedup]

    ax.scatter(xs, ys)

    for cone_id, x, y in dedup:
        ax.text(x + 0.1, y + 0.1, str(cone_id), fontsize=9)

    hull = convex_hull(dedup)

    if len(hull) >= 2:
        hull_x = [c[1] for c in hull] + [hull[0][1]]
        hull_y = [c[2] for c in hull] + [hull[0][2]]
        ax.plot(hull_x, hull_y)

    ax.set_title("Po deduplikacji + otoczka")
    ax.set_aspect("equal")
    ax.grid(True)


m1, original = read_cones("example_input.txt")
m2, dedup = read_cones("deduplicated.txt")

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

plot_input(axes[0], original)
plot_dedup(axes[1], original, dedup)
plot_hull(axes[2], dedup)

plt.tight_layout()
plt.savefig("visualisation.png", dpi=200)