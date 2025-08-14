from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, List
from .engine import World, Character, Faction, Realm
from .events import Event, build_events_trilogy

@dataclass
class SimulationConfig:
    architect_choice: str = "TRINITY"
    smith_rate: float = 0.30
    zion_intensity: float = 0.25
    final_bonus: int = 8

def init_world() -> World:
    w = World()
    w.add(Character("Neo", Faction.HUMAN, realm=Realm.MATRIX, power=20))
    w.add(Character("Trinity", Faction.HUMAN, realm=Realm.MATRIX, power=50))
    w.add(Character("Morpheus", Faction.HUMAN, realm=Realm.MATRIX, power=45))
    w.add(Character("Smith", Faction.PROGRAM, realm=Realm.MATRIX, power=80))
    w.add(Character("Oracle", Faction.PROGRAM, realm=Realm.MATRIX, power=70))
    w.add(Character("Architect", Faction.PROGRAM, realm=Realm.MATRIX, power=90))
    w.add(Character("Keymaker", Faction.PROGRAM, realm=Realm.MATRIX, power=20))
    w.add(Character("Merovingian", Faction.PROGRAM, realm=Realm.MATRIX, power=65))
    w.add(Character("Persephone", Faction.PROGRAM, realm=Realm.MATRIX, power=55))
    return w

def build_trilogy(cfg: SimulationConfig) -> tuple[World, List[Event]]:
    w = init_world()
    events = build_events_trilogy(cfg.architect_choice, cfg.smith_rate, cfg.zion_intensity, cfg.final_bonus)
    return w, events
