#
# vloxx aspect icons (staff, spear, sword), hand drawn vector art traced from
# the weapon references. each weapon is drawn standing up, centered on 0,0 with
# the business end at negative y, then rotated onto the diagonal.
#
# writes svg sources to scripts/icons/vloxx and renders png markers into
# Data/vloxx with headless edge (no python image libraries needed).
#

import math
import subprocess
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parent.parent
svg_folder = root / "scripts/icons/vloxx"
png_folder = root / "Data/vloxx"
size = 128

edge = Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")

# shared palette
outline = "#0a0d26"
crystal_light = "#c4fdff"
crystal = "#5ef0f2"
crystal_dark = "#1fa9c9"
metal = "#5b66c4"
grip = "#2a36b8"
shaft = "#c9d1e3"
star = "#ffffff"

def pts(points):
    return " ".join("%.2f,%.2f" % p for p in points)

def poly(points, fill):
    return '<polygon points="%s" fill="%s"/>' % (pts(points), fill)

def mirror(points):
    return [(-x, y) for x, y in reversed(points)]

def curl(d, width=3.5, color=metal):
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"/>' % (d, color, width)

def mirror_path(d):
    # negate every x in an absolute M/C/L path made of "x,y" pairs
    out = []
    for token in d.split():
        if "," in token:
            prefix = token[0] if token[0].isalpha() else ""
            x, y = token[len(prefix):].split(",")
            out.append("%s%s,%s" % (prefix, -float(x), y))
        else:
            out.append(token)
    return " ".join(out)

def curls(d, width=3.5):
    return curl(d, width) + curl(mirror_path(d), width)

def rhombus(cx, cy, w, h, fill=crystal):
    return poly([(cx, cy - h), (cx + w, cy), (cx, cy + h), (cx - w, cy)], fill)

def starburst(cx, cy, radii, inner, rotation=0):
    # radii are the outer point lengths, evenly spread around the circle
    points = []
    n = len(radii)
    for i, r in enumerate(radii):
        for a, rr in ((i / n, r), ((i + 0.5) / n, inner)):
            angle = math.radians(rotation + a * 360)
            points.append((cx + math.sin(angle) * rr, cy - math.cos(angle) * rr))
    return points

def spike(top, bottom, half_width):
    # crystal spike pointing down, lit from the left
    return (poly([(-half_width, top), (0, top), (0, bottom)], crystal)
            + poly([(0, top), (half_width, top), (0, bottom)], crystal_dark))

def butt_cage(y):
    # small ornate cage holding the bottom spike
    return (curls("M-2,%s C-9,%s -12,%s -7,%s" % (y - 4, y - 3, y + 4, y + 7), 3)
            + '<rect x="-4" y="%s" width="8" height="5" rx="1.5" fill="%s"/>' % (y - 2, metal))

def staff():
    parts = []
    # shaft: wrapped grip above, pale wood below
    parts.append('<rect x="-3.5" y="-34" width="7" height="52" fill="%s"/>' % grip)
    parts.append('<rect x="-3.5" y="18" width="7" height="40" fill="%s"/>' % shaft)
    # vine looping off the head and back into the shaft
    parts.append(curl("M-3,-34 C-24,-22 -20,2 -2,20", 4))
    parts.append(rhombus(0, 22, 4, 6))
    # brilliant cut gem, table up
    parts.append(poly([(-9, -86), (9, -86), (19, -74), (-19, -74)], crystal_light))
    parts.append(poly([(-19, -74), (0, -74), (0, -50)], crystal))
    parts.append(poly([(0, -74), (19, -74), (0, -50)], crystal_dark))
    parts.append(curl("M-3,-86 L-8,-74 M3,-86 L8,-74", 1.2, crystal_dark))
    # cage of scrolls holding the gem
    parts.append(curls("M-3,-36 C-17,-40 -24,-54 -17,-63 C-12,-69 -6,-65 -9,-60", 5))
    parts.append(curls("M-3,-44 C-10,-46 -12,-54 -6,-56", 3))
    parts.append(rhombus(0, -42, 4, 6))
    # bottom spike
    parts.append(butt_cage(58))
    parts.append(spike(64, 90, 6))
    return parts, -45, 0.82

def spear():
    parts = []
    parts.append('<rect x="-3.5" y="-24" width="7" height="36" fill="%s"/>' % grip)
    parts.append('<rect x="-3.5" y="12" width="7" height="44" fill="%s"/>' % shaft)
    # swept wing coming off the collar and wrapping back into the shaft
    parts.append(curl("M0,-22 C-20,-20 -28,0 -12,8 C-6,11 -2,11 0,14", 4))
    parts.append(curl("M0,-22 C10,-24 18,-30 23,-27", 3))
    parts.append(rhombus(0, 14, 4, 6))
    # long crystal head
    parts.append(poly([(0, -94), (0, -52), (-5, -52), (-9, -64)], crystal_light))
    parts.append(poly([(0, -94), (9, -64), (5, -52), (0, -52)], crystal))
    # ornate collar with a hexagonal gem
    parts.append(curls("M-3,-52 C-14,-60 -24,-52 -19,-43 C-16,-37 -10,-39 -12,-44", 4.5))
    parts.append(curls("M-4,-34 C-12,-34 -15,-28 -11,-25", 3))
    hexagon = [(math.sin(math.radians(a)) * 7, -43 - math.cos(math.radians(a)) * 7) for a in range(0, 360, 60)]
    parts.append(poly(hexagon, crystal))
    parts.append(poly([(0, -50), (6, -46.5), (6, -39.5), (0, -43)], crystal_dark))
    parts.append(rhombus(0, -29, 4, 6))
    # bottom spike, longer than the staff's
    parts.append(butt_cage(56))
    parts.append(spike(62, 94, 6))
    return parts, 45, 0.8

def sword():
    parts = []
    parts.append('<defs><linearGradient id="blade" x1="0" y1="-90" x2="0" y2="10" gradientUnits="userSpaceOnUse">'
                 '<stop offset="0" stop-color="#3a50ee"/><stop offset="0.6" stop-color="#9a7cf4"/><stop offset="1" stop-color="#bfe6ff"/></linearGradient></defs>')
    # jagged cosmic blade with a couple of flame tongues breaking off the edges
    right = [(0, -90), (3, -80), (5, -72), (4, -66), (8, -60), (6, -52), (10, -42), (17, -36), (9, -32),
             (13, -22), (10, -12), (14, -4), (12, 8)]
    left = [(-12, 8), (-11, -2), (-19, -10), (-10, -14), (-9, -24), (-12, -34), (-6, -44), (-8, -54),
            (-4, -62), (-6, -70), (-2, -80)]
    parts.append(poly(right + left, "url(#blade)"))
    # constellation running down the blade
    stars = [(0, -82), (2, -64), (-3, -52), (3, -38), (-1, -22), (0, 4)]
    parts.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="1.6" stroke-linejoin="round"/>' % (pts(stars), star))
    for x, y in stars[:-1]:
        parts.append('<circle cx="%s" cy="%s" r="2" fill="%s"/>' % (x, y, star))
    # grip and crystal flame pommel
    parts.append('<rect x="-4" y="16" width="8" height="34" fill="#7cc0ff"/>')
    parts.append('<rect x="-0.8" y="16" width="1.6" height="34" fill="%s"/>' % star)
    pommel = [(0, 46), (6, 51), (11, 48), (9, 57), (13, 64), (6, 63), (3, 73), (0, 66), (-4, 72), (-5, 63),
              (-12, 61), (-8, 55), (-11, 48), (-5, 51)]
    parts.append(poly(pommel, "#8fd6ff"))
    parts.append(poly(starburst(0, 59, [7, 7, 7, 7], 1.5), star))
    # starburst crossguard: long arms across the blade, short ones along it
    parts.append(poly(starburst(0, 12, [22, 12, 16, 26, 38, 26, 14, 12, 18, 12, 14, 26, 38, 26, 16, 12], 8.5), "#9fe9ff"))
    parts.append(poly(starburst(0, 12, [10, 5, 18, 5, 9, 5, 18, 5], 3.5), star))
    return parts, -45, 0.84

def make_svg(parts, rotation, scale):
    # one unified dark outline around the whole silhouette keeps it readable on any floor
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 128 128">'
            '<filter id="outline" x="-10%" y="-10%" width="120%" height="120%">'
            '<feMorphology in="SourceAlpha" operator="dilate" radius="3" result="grown"/>'
            '<feFlood flood-color="{o}"/><feComposite in2="grown" operator="in" result="edge"/>'
            '<feMerge><feMergeNode in="edge"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            '<g filter="url(#outline)"><g transform="translate(64 64) rotate({r}) scale({k})">{p}</g></g></svg>'
            ).format(s=size, o=outline, r=rotation, k=scale, p="".join(parts))

def render(svg_path: Path, png_path: Path, px=size):
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run([str(edge), "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--user-data-dir=" + profile, "--force-device-scale-factor=1",
                        "--default-background-color=00000000", "--window-size=%d,%d" % (px, px),
                        "--screenshot=" + str(png_path), svg_path.as_uri()],
                       check=True, capture_output=True)

def main():
    svg_folder.mkdir(parents=True, exist_ok=True)
    png_folder.mkdir(parents=True, exist_ok=True)
    for name, draw in (("staff", staff), ("spear", spear), ("sword", sword)):
        svg_path = svg_folder / (name + ".svg")
        svg_path.write_text(make_svg(*draw()))
        render(svg_path, png_folder / (name + ".png"))
        print("wrote", png_folder / (name + ".png"))

if __name__ == "__main__":
    main()
