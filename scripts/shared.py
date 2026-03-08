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

def unit_to_gwinch(x):
    return x / 39.3701