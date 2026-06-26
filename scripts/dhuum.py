from shared import make_circle, unit_to_gwinch
import trltools

# east: 403.24, 203.32, 18.33
# south: 398.18, 203.27, 14.18
# west: 395.19, 203.10, 18.16
# north: 398.57, 203.29, 22.52

def main():
    mapid = 1264
    x = 399.215
    y = 203.2
    z = 18.35
    radius = 4.2
    coords = make_circle(x, y, z, radius)
    trltools.write_trl("./Data/dhuum.trl", mapid, coords)

if __name__ == "__main__":
    main()
    