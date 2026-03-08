#
# y is always 129.x
# x is 79, 99, 118
# z is 108, 88, 67, 46
#

from dataclasses import dataclass
from shared import make_circle, unit_to_gwinch
import trltools


@dataclass
class Spear:
    x: float
    y: float
    z: float

spears = [
    Spear(-99.93065878158488, 129.65511055264656, 88.314989565765),
    Spear(-99.97561725340105, 129.45156339693702, 68.00642929215319),
    Spear(-100.19608739801906, 129.4340388946815, 47.46012861957742),
    Spear(-81.67619837532163, 129.6716056609267, 48.57925040294697),
    Spear(-80.87660730319456, 129.5813290495198, 68.2446843881048),
    Spear(-80.1656557339834, 129.59409105434707, 87.24565386390941),
    Spear(-79.70007820219215, 129.97373899386844, 106.1927661910625),
    Spear(-99.08966250720725, 129.99142472650564, 108.15542362732124),
    Spear(-118.3885795271983, 129.53723874129733, 108.52677440335432),
    Spear(-119.20645164414111, 129.43101272444062, 88.45646922569412),
    Spear(-119.2920525744791, 129.44053771929714, 67.8367591201032),
    Spear(-119.47925344995313, 129.49259032790746, 46.464955792712935),
]

def main():
    mapid = 1188
    radius = 310
    coords = []
    for spear in spears:
        radius = unit_to_gwinch(322)
        coords += make_circle(spear.x, spear.y, spear.z, radius)
    trltools.write_trl("./Data/samarog.trl", mapid, coords)

if __name__ == "__main__":
    main()