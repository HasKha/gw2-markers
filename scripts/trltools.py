import struct

def write_trl(path, mapid, coords: list[list[float]]):
    f = open(path, "wb")
    f.write(struct.pack("i", 0))
    f.write(struct.pack("i", mapid))
    for coord in coords:
        f.write(struct.pack("fff", coord[0], coord[1], coord[2]))

def read_trl(path):
    f = open(path, "rb")
    version = struct.unpack("i", f.read(4))[0] # 4 bytes are version information. should be 0.
    if version != 0:
        return None # something is wrong
    mapid = struct.unpack("i", f.read(4))[0] # 4 bytes for map id
    # then it's just series of float xyz
    coords = []
    while True:
        chunk = f.read(12)
        if not chunk:
            break
        x, y, z = struct.unpack("fff", chunk)
        coords.append([x, y, z])
    return mapid, coords

def main():
    path = "./Data/ura/safe_areas.trl"
    mapid, coords = read_trl(path)
    for coord in coords:
        print(coord)

if __name__ == "__main__":
    main()
