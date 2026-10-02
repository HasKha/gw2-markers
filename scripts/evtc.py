#
# evtc / zevtc reader. format reference:
#   https://www.deltaconnected.com/arcdps/evtc/README.txt
#   https://www.deltaconnected.com/arcdps/evtc/writeencounter.cpp
#
# usage:
#   log = evtc.load("path/to/log.zevtc")
#   for ev in log.events_of(evtc.SC.POSITION): ...
#

import struct
import zipfile
from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path

LOG_FOLDER = Path.home() / "Documents/Guild Wars 2/addons/arcdps/arcdps.cbtlogs"

class SC(IntEnum):
    # cbtstatechange, values must match the arcdps enum exactly
    COMBAT = 0
    ENTERCOMBAT = 1
    EXITCOMBAT = 2
    CHANGEUP = 3
    CHANGEDEAD = 4
    CHANGEDOWN = 5
    SPAWN = 6
    DESPAWN = 7
    HEALTHPCTUPDATE = 8
    SQCOMBATSTART = 9
    SQCOMBATEND = 10
    WEAPSWAP = 11
    MAXHEALTHUPDATE = 12
    POINTOFVIEW = 13
    LANGUAGE = 14
    GWBUILD = 15
    SHARDID = 16
    REWARD = 17
    BUFFINITIAL = 18
    POSITION = 19
    VELOCITY = 20
    FACING = 21
    TEAMCHANGE = 22
    ATTACKTARGET = 23
    TARGETABLE = 24
    MAPID = 25
    REPLINFO = 26
    BUFFACTIVE = 27
    BUFFDEACTIVE = 28
    GUILD = 29
    BUFFINFO = 30
    BUFFFORMULA = 31
    SKILLINFO = 32
    SKILLTIMING = 33
    DEFIANCEBARSTATE = 34
    DEFIANCEBARPERCENT = 35
    INTEGRITY = 36
    MARKER = 37
    BARRIERPCTUPDATE = 38
    STATRESET_DEFUNC = 39
    EXTENSION = 40
    APIDELAYED_DEFUNC = 41
    INSTANCESTART = 42
    RATEHEALTH = 43
    LAST90BEFOREDOWN_DEFUNC = 44
    EFFECT1_DEFUNC = 45
    IDTOGUID = 46
    LOGNPCUPDATE = 47
    IDLEEVENT = 48
    EXTENSIONCOMBAT = 49
    FRACTALSCALE = 50
    EFFECT2_DEFUNC = 51
    RULESET = 52
    SQUADMARKER_GROUND = 53
    ARCBUILD = 54
    GLIDER = 55
    STUNBREAK = 56
    MISSILECREATE = 57
    MISSILELAUNCH = 58
    MISSILEREMOVE = 59
    EFFECTGROUNDCREATE = 60
    EFFECTGROUNDREMOVE = 61
    EFFECTAGENTCREATE = 62
    EFFECTAGENTREMOVE = 63
    IIDCHANGE = 64
    MAPCHANGE = 65
    EARLYEXIT = 66
    ANIMATIONSTART = 67
    ANIMATIONSTOP = 68
    BUFFAPPLY = 69
    BUFFCHANGE = 70
    BUFFREMOVE_SINGLE = 71
    BUFFREMOVE_ALL = 72
    TRANSFORMATION = 73
    WVWTEAMS = 74
    WVWOBJECTIVESTATUS = 75
    STEALTHCHANGE = 76
    GADGETANIMATION = 77
    GADGETNAME = 78
    MISSILEEFFECT = 79
    GADGETCAPTUREOUTLINESHOW = 80
    GADGETCAPTURESPLITPERCENT = 81
    GADGETCAPTUREOUTLINEHIDE = 82
    GADGETCAPTUREOUTLINEPOINT = 83
    TICK = 84
    TELEPORT = 85
    JUMP = 86
    GADGETMODELINFO = 87
    FLYTO = 88
    AGENTINFO = 89

AGENT_STRUCT = struct.Struct("<QIIhhhHhH64s4x") # 96 bytes, padded to 8
SKILL_STRUCT = struct.Struct("<i64s")
EVENT_STRUCT = struct.Struct("<QQQiiIIHHHH16B") # revision 1, 64 bytes

@dataclass
class Agent:
    addr: int
    prof: int
    is_elite: int
    hitbox_width: int
    hitbox_height: int
    name: str
    # filled in from events
    instid: int = 0
    first_aware: int = 0
    last_aware: int = 2**64 - 1

    @property
    def is_player(self):
        return self.is_elite != 0xFFFFFFFF

    @property
    def is_gadget(self):
        return not self.is_player and (self.prof >> 16) == 0xFFFF

    @property
    def is_npc(self):
        return not self.is_player and not self.is_gadget

    @property
    def species(self):
        # species id for npcs, volatile pseudo id for gadgets
        return self.prof & 0xFFFF

@dataclass(slots=True)
class Event:
    time: int
    src_agent: int
    dst_agent: int
    value: int
    buff_dmg: int
    overstack_value: int
    skillid: int
    src_instid: int
    dst_instid: int
    src_master_instid: int
    dst_master_instid: int
    iff: int
    buff: int
    result: int
    is_activation: int
    is_buffremove: int
    is_ninety: int
    is_fifty: int
    is_moving: int
    is_statechange: int
    is_flanking: int
    is_shields: int
    is_offcycle: int
    pad: tuple
    raw: bytes

    def floats(self, offset=16, count=3):
        # positional statechanges pack float[] into dst_agent (offset 16)
        return struct.unpack_from("<%df" % count, self.raw, offset)

@dataclass
class Log:
    path: Path
    build: str
    revision: int
    boss_id: int
    agents: list
    skills: dict
    events: list
    by_addr: dict = field(default_factory=dict)
    map_id: int = 0
    combat_start: int = 0 # time of SQCOMBATSTART
    combat_end: int = 0   # time of SQCOMBATEND
    log_start: int = 0    # time of first event

    def events_of(self, statechange):
        return [e for e in self.events if e.is_statechange == statechange]

    def agents_named(self, name):
        return [a for a in self.agents if a.name == name]

    def agents_species(self, species):
        return [a for a in self.agents if a.is_npc and a.species == species]

    def rel(self, time):
        # seconds since squad combat start
        return (time - self.combat_start) / 1000

def _read_bytes(path: Path):
    if path.suffix == ".zevtc":
        with zipfile.ZipFile(path) as z:
            return z.read(z.namelist()[0])
    return path.read_bytes()

def _cstr(b: bytes):
    return b.split(b"\0", 1)[0].decode("utf8", errors="replace")

def load(path) -> Log:
    path = Path(path)
    data = _read_bytes(path)
    assert data[0:4] == b"EVTC", "not an evtc file"
    build = data[4:12].decode()
    revision = data[12]
    assert revision == 1, "only revision 1 is supported"
    boss_id = struct.unpack_from("<H", data, 13)[0]
    offset = 16

    agent_count = struct.unpack_from("<I", data, offset)[0]
    offset += 4
    agents = []
    for i in range(agent_count):
        (addr, prof, is_elite, _toughness, _concentration, _healing, hitbox_width,
         _condition, hitbox_height, name) = AGENT_STRUCT.unpack_from(data, offset)
        offset += AGENT_STRUCT.size
        # players: "character\0account\0subgroup\0" -> keep the character name
        agents.append(Agent(addr, prof, is_elite, hitbox_width, hitbox_height, _cstr(name)))

    skill_count = struct.unpack_from("<I", data, offset)[0]
    offset += 4
    skills = {}
    for i in range(skill_count):
        sid, name = SKILL_STRUCT.unpack_from(data, offset)
        offset += SKILL_STRUCT.size
        skills[sid] = _cstr(name)

    events = []
    for off in range(offset, len(data) - EVENT_STRUCT.size + 1, EVENT_STRUCT.size):
        f = EVENT_STRUCT.unpack_from(data, off)
        events.append(Event(*f[:11], *f[11:23], f[23:27], data[off:off + 64]))

    log = Log(path, build, revision, boss_id, agents, skills, events)
    log.by_addr = {a.addr: a for a in agents}
    _assign_awareness(log)
    for e in events:
        if e.is_statechange == SC.MAPID:
            log.map_id = e.src_agent
        elif e.is_statechange == SC.SQCOMBATSTART and not log.combat_start:
            log.combat_start = e.time
        elif e.is_statechange == SC.SQCOMBATEND:
            log.combat_end = e.time
    if events:
        log.log_start = events[0].time
        if not log.combat_start:
            log.combat_start = log.log_start
    return log

def _assign_awareness(log: Log):
    # as described in README: instid from non-statechange events, first/last aware from any event
    seen = set()
    for e in log.events:
        a = log.by_addr.get(e.src_agent)
        if a is None:
            continue
        if not e.is_statechange and not a.instid:
            a.instid = e.src_instid
        if a.addr not in seen:
            seen.add(a.addr)
            a.first_aware = e.time
        a.last_aware = e.time

def convert_position_from_arc(position):
    # arc position is in inches, x/y horizontal, z down.
    # marker (mumble) position is in meters, x/z horizontal, y up.
    x = position[0] / 39.3701
    y = -position[2] / 39.3701
    z = position[1] / 39.3701
    return (x, y, z)

def log_files(folder):
    folder = Path(folder)
    return sorted(list(folder.glob("*.zevtc")) + list(folder.glob("*.evtc")))

def print_positions(path, name_to_track):
    # header info, then every distinct position of agents whose name contains name_to_track
    log = load(path)
    print("revision:", log.revision, "build:", log.build, "boss id:", log.boss_id, "map id:", log.map_id)
    print("num agents:", len(log.agents), "num skills:", len(log.skills), "num events:", len(log.events))
    tracked = {a.addr for a in log.agents if name_to_track in a.name}
    for a in log.agents:
        if a.addr in tracked:
            print(a.name)
    positions = []
    for e in log.events_of(SC.POSITION):
        if e.src_agent in tracked:
            position = convert_position_from_arc(e.floats())
            if position not in positions:
                positions.append(position)
    for position in positions:
        print(position)

def main():
    # python evtc.py [log path] [agent name substring]
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "./logs/20260301-184848.evtc"
    name_to_track = sys.argv[2] if len(sys.argv) > 2 else "Spear of"
    print_positions(path, name_to_track)

if __name__ == "__main__":
    main()
