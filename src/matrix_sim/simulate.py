from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Dict, Any, List, Optional
import json
from .engine import World
from .events import Event

@dataclass
class TimelineSimulator:
    world: World
    jsonl_path: Optional[str] = None

    def _emit(self, rec: Dict[str, Any]) -> None:
        if not self.jsonl_path: return
        with open(self.jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def run(self, events: Iterable[Event]) -> World:
        self.world.log_event(movie=self._m("Prelude"), event="Start",
                             desc="Matrix exists; Neo asleep; Machines rule.",
                             themes=["CONTROL_SYSTEMS"], myth=[])
        self._emit(self.world.log[-1])
        for e in events:
            before = len(self.world.log)
            e.run(self.world)
            if len(self.world.log) > before:
                self._emit(self.world.log[-1])
        self.world.log_event(movie=self._m("Epilogue"), event="End",
                             desc="Simulation finished.", themes=["HUMAN_MACHINE_SYMBIOSIS"], myth=[])
        self._emit(self.world.log[-1])
        return self.world

    @staticmethod
    def _m(name: str):
        # lightweight pseudo-movie bucket for non-film entries
        from types import SimpleNamespace
        class MM:  # simple enum-ish shim with .value
            def __init__(self, v): self.value = v
        return MM(name)

def format_timeline(log: List[Dict[str, Any]]) -> str:
    out, current = [], None
    for rec in log:
        if rec["movie"] != current:
            current = rec["movie"]
            out.append(f"\n=== {current} ===")
        out.append(f"- {rec['event']}: {rec['desc']} | themes={rec['themes']} myth={rec['myth']} | snapshot={rec['snapshot']}")
    return "\n".join(out)
