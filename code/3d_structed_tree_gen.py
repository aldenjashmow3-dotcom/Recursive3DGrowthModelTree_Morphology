import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ---------------------------------------------------------
# 1. Seed → Spiral
# ---------------------------------------------------------
def seed_spiral(n=300, height=2, radius=0.2):
    t = np.linspace(0, 6*np.pi, n)
    x = radius * np.cos(t)
    y = radius * np.sin(t)
    z = np.linspace(0, height, n)
    return x, y, z

# ---------------------------------------------------------
# 2. Helix (Trunk)
# ---------------------------------------------------------
def helix(n=400, height=6, radius=0.1):
    t = np.linspace(0, 10*np.pi, n)
    x = radius * np.cos(t)
    y = radius * np.sin(t)
    z = np.linspace(0, height, n)
    return x, y, z

# ---------------------------------------------------------
# 3. Recursive Branching
# ---------------------------------------------------------
def branch(origin, direction, depth, length):
    if depth == 0:
        return []

    ox, oy, oz = origin
    dx, dy, dz = direction

    # endpoint of this branch
    end = np.array([ox + dx*length, oy + dy*length, oz + dz*length])

    # generate small random jitter for bark-like texture
    jitter = (np.random.rand(3) - 0.5) * 0.1
    end = end + jitter

    branches = [(origin, end)]

    # recursive sub-branches
    for angle in [np.pi/6, -np.pi/6]:
        rot = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle),  np.cos(angle), 0],
            [0, 0, 1]
        ])
        new_dir = rot @ direction
        branches += branch(end, new_dir, depth-1, length*0.7)

    return branches

# ---------------------------------------------------------
# 4. Canopy (Spherical distribution)
# ---------------------------------------------------------
def canopy(center, radius=1.5, points=800):
    phi = np.random.rand(points) * 2*np.pi
    costheta = np.random.rand(points) * 2 - 1
    u = np.random.rand(points)

    theta = np.arccos(costheta)
    r = radius * (u ** (1/3))

    x = center[0] + r * np.sin(theta) * np.cos(phi)
    y = center[1] + r * np.sin(theta) * np.sin(phi)
    z = center[2] + r * np.cos(theta)

    return x, y, z

# ---------------------------------------------------------
# Plotting
# ---------------------------------------------------------
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection='3d')

# Seed spiral
xs, ys, zs = seed_spiral()
ax.scatter(xs, ys, zs, s=2, color='gold')

# Helix trunk
xh, yh, zh = helix()
ax.scatter(xh, yh, zh, s=2, color='white')

# Branches
origin = np.array([0,0,6])
direction = np.array([0,1,1])
branches = branch(origin, direction, depth=4, length=2)

for start, end in branches:
    ax.plot([start[0], end[0]],
            [start[1], end[1]],
            [start[2], end[2]],
            color='white', linewidth=1)

# Canopy
xc, yc, zc = canopy(center=[0,0,8])
ax.scatter(xc, yc, zc, s=3, color='lightgreen')

ax.set_facecolor("black")
plt.show()
