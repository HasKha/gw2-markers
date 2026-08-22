import math

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

def make_meridian(x, y, z, radius, bearing, elev_start=0, elev_end=180, angle_step=5):
    # vertical great-circle arc on a sphere. bearing picks the horizontal plane
    # the arc lies in, elevation runs from 0 (ground, +bearing side) through
    # 90 (top) to 180 (ground, opposite side).
    coords = []
    bearing_rad = math.radians(bearing)
    dirX = math.cos(bearing_rad)
    dirZ = math.sin(bearing_rad)
    for elev_deg in range(elev_start, elev_end + 1, angle_step):
        elev_rad = math.radians(elev_deg)
        posX = x + dirX * math.cos(elev_rad) * radius
        posY = y + math.sin(elev_rad) * radius
        posZ = z + dirZ * math.cos(elev_rad) * radius
        coords.append([posX, posY, posZ])
    coords.append([0, 0, 0])
    return coords

def unit_to_gwinch(x):
    return x / 39.3701
