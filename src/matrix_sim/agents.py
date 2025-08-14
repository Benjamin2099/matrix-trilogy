from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Callable
import random
from .engine import World
from .events import (
    Event,
    ev_awaken_neo, ev_train_neo, ev_rescue_morpheus, ev_neo_ascends,
    ev_smith_spreads, ev_smith_copies_oracle,
    ev_zion_assault, ev_machines_negotiate, ev_final_fight, ev_peace
)

Action = Callable[[World], None]

@dataclass
class Agent:
    name: str
    rng: random.Random
    def choose(self, w: World) -> Optional[Event]:
        return None

class NeoAgent(Agent):
    def choose(self, w: World) -> Optional[Event]:
        if not w.neo_awake:
            return ev_awaken_neo()
        if w.get("Neo").power < 60:
            return ev_train_neo()
        if w.smith_factor > 0.6:
            # Negotiate then fight in same tick via two events
            return ev_machines_negotiate()
        # default: assert dominance
        return ev_neo_ascends()

class SmithAgent(Agent):
    def choose(self, w: World) -> Optional[Event]:
        if w.smith_factor < 0.6:
            return ev_smith_spreads(0.25)
        return ev_smith_copies_oracle()

class MachineCollectiveAgent(Agent):
    """Sentinels pressure; negotiate when Smith is existential."""
    def choose(self, w: World) -> Optional[Event]:
        if w.smith_factor >= 0.75:
            return ev_machines_negotiate()
        if w.zion_alive and w.zion_defense > 0:
            return ev_zion_assault(0.2)
        return None

@dataclass
class AgentSimulator:
    world: World
    rng: random.Random
    max_ticks: int = 12

    def run(self, agents: List[Agent]) -> World:
        self.world.log_event(self._m("Prelude"), "Start", "Agent mode: Neo, Smith, Machines act per tick.", [], [])
        for t in range(self.max_ticks):
            self.world.log_event(self._m("Tick"), f"T{t+1}", "Decision phase.", [], [])
            # Each agent proposes one event
            chosen: List[Event] = []
            for a in agents:
                ev = a.choose(self.world)
                if ev: chosen.append(ev)
            # Apply each event
            for ev in chosen:
                ev.run(self.world)
                # optional: if Neo negotiated and Smith is high, try immediate fight
                if ev.name.startswith("Machines negotiate") and self.world.smith_factor >= 0.6:
                    ev_final_fight(8).run(self.world)
            # Check peace condition each tick
            ev_peace().run(self.world)
            if self.world.peace or not self.world.zion_alive:
                break
        self.world.log_event(self._m("Epilogue"), "End", "Agent simulation finished.", [], [])
        return self.world

    @staticmethod
    def _m(name: str):
        class MM:
            def __init__(self, v): self.value = v
        return MM(name)
