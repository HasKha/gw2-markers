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
import trltools

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
    Geyser(183.057, 269.856, 235.223, "heart", 0, 0),
    Geyser(165.245, 269.916, 253.156, "cloud", 0, 0),
    Geyser(158.040, 269.937, 280.916, "x", 28, 205),
    Geyser(178.847, 269.904, 202.339, "arrow", -116, 7),
    Geyser(161.718, 269.887, 228.767, "square", 0, 0),
    Geyser(145.961, 269.847, 259.399, "star", 97, 169),
    Geyser(162.641, 269.851, 200.383, "cat", -147, -50),
    Geyser(145.577, 269.847, 228.939, "fox", 0, 0),
    Geyser(122.405, 269.845, 249.628, "plus", 56, 235),
    Geyser(136.756, 269.853, 199.693, "frog", -200, -30),
    Geyser(109.507, 269.864, 218.631, "fish", 80, 310),
]

@dataclass
class Spawner:
    x: float
    y: float
    z: float

spawners = [
    Spawner(141.47, 268.34, 210.48),
    Spawner(171.51, 268.33, 218.83),
    Spawner(150.50, 268.34, 255.44),
    Spawner(176.85, 268.27, 243.99),
    Spawner(128.84, 268.36, 234.44),
]

def unit_to_gwinch(x):
    return x / 39.3701

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
    r = unit_to_gwinch(600)
    circle_intersections(g1.x, g1.z, g2.x, g2.z, r, g1.name, g2.name)

# find_intersection_angles(star, plus)


def make_arc(x, y, z, radius, angle_start, angle_end, angle_step):
    if angle_start == angle_end:
        return []
    coords = []
    count = angle_end - angle_start + 1
    for angle_deg in range(angle_start, angle_end + 1, angle_step):
        angle_rad = math.radians(angle_deg)
        posX = x + math.cos(angle_rad) * radius
        posY = y
        posZ = z + math.sin(angle_rad) * radius
        coords.append([posX, posY, posZ])
    coords.append([0, 0, 0])
    return coords

def make_circle(x, y, z, radius):
    return make_arc(x, y, z, radius, 0, 360, 5)

def save_safe_drop_arcs():
    radius = unit_to_gwinch(600)
    coords = []
    for geyser in geysers:
        coords += make_arc(geyser.x, geyser.y, geyser.z, radius, geyser.angleStart, geyser.angleEnd, 2)
    trltools.write_trl("./Data/ura/safe_areas.trl", mapid, coords)


def save_hitboxes():
    # toxic hitbox is 80
    # toxic SAK range is 80 + 170 - 24 = 226
    # spawner hitbox is 105
    # spawner SAK range is 105 + 170 - 24 = 251
    coords = []
    for geyser in geysers:
        radius = unit_to_gwinch(80)
        coords += make_circle(geyser.x, geyser.y, geyser.z, radius)
    trltools.write_trl("./Data/ura/toxic_hitbox.trl", mapid, coords)

    coords = []
    for geyser in geysers:
        radius = unit_to_gwinch(226)
        coords += make_circle(geyser.x, geyser.y, geyser.z, radius)
    trltools.write_trl("./Data/ura/toxic_sak.trl", mapid, coords)

    coords = []
    for spawner in spawners:
        radius = unit_to_gwinch(105)
        coords += make_circle(spawner.x, spawner.y, spawner.z, radius)
    trltools.write_trl("./Data/ura/spawner_hitbox.trl", mapid, coords)

    coords = []
    for spawner in spawners:
        radius = unit_to_gwinch(251)
        coords += make_circle(spawner.x, spawner.y, spawner.z, radius)
    trltools.write_trl("./Data/ura/spawner_sak.trl", mapid, coords)
    

def main():
    save_safe_drop_arcs()
    save_hitboxes()


if __name__ == "__main__":
    main()
