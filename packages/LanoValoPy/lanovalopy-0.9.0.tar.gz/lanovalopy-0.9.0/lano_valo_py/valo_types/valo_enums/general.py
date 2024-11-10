from enum import Enum


class Modes(str, Enum):
    escalation = "escalation"
    spikerush = "spikerush"
    deathmatch = "deathmatch"
    competitive = "competitive"
    unrated = "unrated"
    replication = "replication"
    custom = "custom"
    newmap = "newmap"
    snowball = "snowball"


class Maps(str, Enum):
    ascent = "ascent"
    split = "split"
    fracture = "fracture"
    bind = "bind"
    breeze = "breeze"
    icebox = "icebox"
    haven = "haven"
    pearl = "pearl"


class RawTypes(str, Enum):
    competitiveupdates = "competitiveupdates"
    mmr = "mmr"
    matchdetails = "matchdetails"
    matchhistory = "matchhistory"


class Patforms(str, Enum):
    pc = "PC"
    console = "CONSOLE"
