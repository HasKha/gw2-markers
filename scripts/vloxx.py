#
# vloxx log analysis.
#
#   python vloxx.py spawns   - where the aspect adds (staff, spear, sword) spawn
#
# positions are printed in marker coordinates (x, y up, z).
#

import sys
from collections import defaultdict
from dataclasses import dataclass
import evtc
from evtc import SC

mapid = 1638
boss_species = 28106
log_folder = evtc.LOG_FOLDER / "Vloxx (28106)"

# any npc whose name starts with this is an add we care about
add_prefix = "Aspect of the"

# a position update further than this from the spawn event means the add
# spawned out of the pov's range, so the first position is not the spawn point
max_spawn_delay = 0.5 # seconds

@dataclass
class Spawn:
    log: str
    name: str
    species: int
    time: float # seconds since squad combat start
    pos: tuple  # marker coords
    delay: float # seconds between spawn and first position update

def find_spawns(log: evtc.Log):
    adds = {a.addr: a for a in log.agents if a.is_npc and a.name.startswith(add_prefix)}
    spawned = {} # addr -> spawn time
    found = set()
    spawns = []
    for e in log.events:
        if e.src_agent not in adds or e.src_agent in found:
            continue
        if e.is_statechange == SC.SPAWN:
            spawned[e.src_agent] = e.time
        elif e.is_statechange == SC.POSITION:
            a = adds[e.src_agent]
            t0 = spawned.get(a.addr, a.first_aware)
            pos = evtc.convert_position_from_arc(e.floats())
            spawns.append(Spawn(log.path.name, a.name, a.species, log.rel(t0), pos, (e.time - t0) / 1000))
            found.add(a.addr)
    return spawns

def is_cm(log: evtc.Log):
    return any(a.name == "Challenge Mote" for a in log.agents)

def all_spawns():
    spawns = []
    for path in evtc.log_files(log_folder):
        log = evtc.load(path)
        if log.boss_id != boss_species:
            continue
        spawns += find_spawns(log)
    return spawns

def report_spawns():
    spawns = all_spawns()
    by_name = defaultdict(list)
    for s in spawns:
        by_name[s.name].append(s)
    print("logs:", len({s.log for s in spawns}), "adds:", len(spawns))
    for name, group in sorted(by_name.items()):
        good = [s for s in group if s.delay <= max_spawn_delay]
        late = [s for s in group if s.delay > max_spawn_delay]
        print()
        print("%s (species %s): %d spawns, %d with late first position"
              % (name, sorted({s.species for s in group}), len(group), len(late)))
        # cluster spawn positions at 1cm
        clusters = defaultdict(list)
        for s in good:
            key = tuple(round(v, 2) for v in s.pos)
            clusters[key].append(s)
        for key, members in sorted(clusters.items(), key=lambda kv: -len(kv[1])):
            print("  %4d x  x=%.3f y=%.3f z=%.3f" % (len(members), *key))
        for s in late:
            print("  late: %s t=%.1f delay=%.1f pos=(%.3f, %.3f, %.3f)" % (s.log, s.time, s.delay, *s.pos))

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "spawns"
    if cmd == "spawns":
        report_spawns()

if __name__ == "__main__":
    main()
