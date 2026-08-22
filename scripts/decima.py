#
# dome over the arena. center + radius fitted from the 7 points in w8.trl:
# 6 rough edge points trace a quarter meridian from straight overhead down to
# the horizon, all 61.5 - 62.1 from the 7th point. sphere fit rms 0.19,
# ellipsoid fit gives b/a = 0.997 and a capsule collapses to height 0,
# so it really is a sphere / dome.
#

from shared import make_meridian
import trltools

mapid = 1564

# center of the dome (last point of w8.trl)
x = -259.930
y = 138.522
z = 334.204

radius = 62.0

# two axis aligned meridians and two on the diagonals between them
bearings = [0, 45, 90, 135]

# elevation the arcs span. clipped off the ground ends so they stop short of the floor
elev_start = 35
elev_end = 145

def save_dome():
    coords = []
    for bearing in bearings:
        coords += make_meridian(x, y, z, radius, bearing, elev_start, elev_end, angle_step=2)
    trltools.write_trl("./Data/decima.trl", mapid, coords)

def main():
    save_dome()

if __name__ == "__main__":
    main()
