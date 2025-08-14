from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Any

class Movie(Enum):
    MATRIX = "Matrix (1999)"
    RELOADED = "Matrix Reloaded (2003)"
    REVOLUTIONS = "Matrix Revolutions (2003)"

class Realm(Enum):
    MATRIX = auto()
    REAL = auto()
    LIMINAL = auto()  # Train Station / between-worlds

class Faction(Enum):
    HUMAN = auto()
    MACHINE = auto()
    PROGRAM = auto()

class Theme(Enum):
    REALITY_ILLUSION = auto()
    FREE_WILL = auto()
    DETERMINISM = auto()
    CONTROL_SYSTEMS = auto()
    LOVE_SACRIFICE = auto()
    HUMAN_MACHINE_SYMBIOSIS = auto()
    SMITH_SHADOW = auto()
    MESSIANIC_GNOSIS = auto()
    UNDERWORLD_PASSAGES = auto()

@dataclass
class Character:
    name: str
    faction: Faction
    realm: Realm = Realm.MATRIX
    alive: bool = True
    power: int = 10  # rough 0..100

@dataclass
class World:
    # macro state
    matrix_control: float = 1.0
    zion_defense: float = 0.4
    smith_factor: float = 0.0
    humans_free: int = 1_000
    humans_enslaved: int = 1_000_000_000
    peace: bool = False
    prophecy_valid: bool = True

    # flags
    neo_awake: bool = False
    neo_alive: bool = True
    trinity_alive: bool = True
    zion_alive: bool = True

    # registry & log
    chars: Dict[str, Character] = field(default_factory=dict)
    log: List[dict] = field(default_factory=list)

    def add(self, c: Character) -> None:
        self.chars[c.name] = c

    def get(self, name: str) -> Character:
        return self.chars[name]

    def snapshot(self) -> Dict[str, Any]:
        return {
            "matrix_control": round(self.matrix_control, 3),
            "zion_defense": round(self.zion_defense, 3),
            "smith_factor": round(self.smith_factor, 3),
            "humans_free": self.humans_free,
            "humans_enslaved": self.humans_enslaved,
            "neo_awake": self.neo_awake,
            "neo_alive": self.neo_alive,
            "trinity_alive": self.trinity_alive,
            "zion_alive": self.zion_alive,
            "peace": self.peace,
            "prophecy_valid": self.prophecy_valid,
        }

    def log_event(self, movie: Movie, event: str, desc: str, themes: list[str], myth: list[str]) -> None:
        self.log.append({
            "movie": movie.value,
            "event": event,
            "desc": desc,
            "themes": themes,
            "myth": myth,
            "snapshot": self.snapshot(),
        })
