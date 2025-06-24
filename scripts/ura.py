import matplotlib.patches
import matplotlib.pyplot as plt

geyser_locations = [
    [196.7, 247.2, 269.7],
    [181.6, 276.9, 269.9],
    [193.8, 219.2, 269.8],
    [183.0, 235.2, 269.8],
    [165.2, 253.1, 269.9],
    [158.0, 280.9, 269.9],
    [178.8, 202.3, 269.9],
    [161.7, 228.7, 269.8],
    [145.9, 259.3, 269.8],
    [162.6, 200.3, 269.8],
    [145.5, 228.9, 269.8],
    [122.4, 249.6, 269.8],
    [136.7, 199.6, 269.8],
    [109.5, 218.6, 269.8],
]
radius = 15
fig, ax = plt.subplots()
fig.set_size_inches(50, 50)
ax.set_axis_off()
xMax = -1000
xMin = 1000
yMax = -1000
yMin = 1000
for loc in geyser_locations:
    x = loc[0]
    y = loc[1]
    xMax = max(xMax, x)
    xMin = min(xMin, x)
    yMax = max(yMax, y)
    yMin = min(yMin, y)
    circle = matplotlib.patches.Circle((x, y), radius)
    ax.add_patch(circle)
margin = radius * 2
ax.set_xlim((xMin - margin, xMax + margin))
ax.set_ylim((yMin - margin, yMax + margin))
# matplotlib.pyplot.show()
fig.savefig("test.png")
