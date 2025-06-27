# generates content to copy into the TrlTool
# blishhud:
#       +z 
#   -x      +x
#       -z
# positive y up
#
# trl:
#       +y
#   -x      +x
#       -y
# positive z up

from dataclasses import dataclass
import math

mapid = 1564

@dataclass
class Geyser:
    x: float
    y: float
    z: float
    name: str
    angleStart: int = 0
    angleEnd: int = 360

geysers = [
    Geyser(196.736, 269.771, 247.251, "spiral", -73, 100),
    Geyser(181.636, 269.910, 276.953, "triangle", -45, 132),
    Geyser(193.879, 269.820, 219.205, "circle", -90, 62),
    Geyser(158.040, 269.937, 280.916, "x", 28, 205),
    Geyser(178.847, 269.904, 202.339, "arrow", -116, 7),
    Geyser(145.961, 269.847, 259.399, "star", 97, 169),
    Geyser(162.641, 269.851, 200.383, "cat", -147, -50),
    Geyser(122.405, 269.845, 249.628, "plus", 56, 235),
    Geyser(136.756, 269.853, 199.693, "frog", -200, -30),
    Geyser(109.507, 269.864, 218.631, "fish", 80, 310),
]
spiral = geysers[0]
triangle = geysers[1]
circle = geysers[2]
x = geysers[3]
arrow = geysers[4]
star = geysers[5]
cat = geysers[6]
plus = geysers[7]
frog = geysers[8]
fish = geysers[9]


def unit_to_gwinch(x):
    return x / 39.3701

r = unit_to_gwinch(600)

def circle_intersections(x1, y1, x2, y2, r, name1, name2):
    dx = x2 - x1
    dy = y2 - y1
    d = math.hypot(dx, dy)

    if d > 2 * r or d == 0:
        return None  # no or infinite intersections

    a = d / 2
    h = math.sqrt(r**2 - a**2)

    xm = x1 + dx * 0.5
    ym = y1 + dy * 0.5

    rx = -dy * (h / d)
    ry = dx * (h / d)

    xi1 = xm + rx
    yi1 = ym + ry
    xi2 = xm - rx
    yi2 = ym - ry

    # angles from x-axis
    angle1_1 = math.degrees(math.atan2(yi1 - y1, xi1 - x1))
    angle1_2 = math.degrees(math.atan2(yi2 - y1, xi2 - x1))

    angle2_1 = math.degrees(math.atan2(yi1 - y2, xi1 - x2))
    angle2_2 = math.degrees(math.atan2(yi2 - y2, xi2 - x2))

    print("points: ({}, {}), ({}, {})".format(xi1, yi1, xi2, yi2))
    print("angles {}: {}, {}".format(name1, angle1_1, angle1_2))
    print("angles {}: {}, {}".format(name2, angle2_1, angle2_2))

def find_intersection_angles(g1: Geyser, g2: Geyser):
    circle_intersections(g1.x, g1.z, g2.x, g2.z, r, g1.name, g2.name)

find_intersection_angles(star, plus)

num_segments = 360
for geyser in geysers:
    file = open("./scripts/tmp/" + geyser.name + ".txt", "w")
    file.write("M1564\n")
    count = geyser.angleEnd - geyser.angleStart + 1
    print(geyser.name)
    for i in range(count):
        angleDeg = geyser.angleStart + i
        angleRad = math.radians(angleDeg)
        posX = geyser.x + math.cos(angleRad) * r
        posY = geyser.z + math.sin(angleRad) * r
        if i == 0:
            print("({}, {})".format(posX, posY))
        if i == (count - 1):
            print("({}, {})".format(posX, posY))
        file.write(str(posX) + " " + str(posY) + " " + str(geyser.y) + "\n")