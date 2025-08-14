from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Optional, Set, List
from .engine import World, Movie, Theme, Realm

def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))

@dataclass
class Event:
    movie: Movie
    name: str
    desc: str
    themes: Set[Theme]
    myth: List[str]
    pre: Optional[Callable[[World], bool]] = None
    effect: Optional[Callable[[World], None]] = None

    def run(self, w: World) -> bool:
        if self.pre and not self.pre(w):
            w.log_event(self.movie, f"[SKIP] {self.name}", "Precondition failed", [t.name for t in self.themes], self.myth)
            return False
        if self.effect:
            self.effect(w)
        w.log_event(self.movie, self.name, self.desc, [t.name for t in self.themes], self.myth)
        return True

# ---- Event factories (Matrix I–III + Machines) ----

def ev_awaken_neo() -> Event:
    def effect(w: World):
        w.neo_awake = True
        w.get("Neo").realm = Realm.REAL
        w.get("Neo").power = max(w.get("Neo").power, 30)
        w.humans_free += 1
        w.matrix_control = _clamp01(w.matrix_control - 0.02)
    return Event(Movie.MATRIX, "Neo awakens (Red Pill)",
                 "Morpheus frees Neo; reality revealed as simulation.",
                 {Theme.REALITY_ILLUSION, Theme.MESSIANIC_GNOSIS, Theme.FREE_WILL},
                 ["Gnosis (revelation)"], effect=effect)

def ev_train_neo() -> Event:
    return Event(Movie.MATRIX, "Training (Kung Fu, Bullet Time)",
                 "Neo bends Matrix rules via training.",
                 {Theme.REALITY_ILLUSION, Theme.CONTROL_SYSTEMS}, [],
                 pre=lambda w: w.neo_awake,
                 effect=lambda w: (setattr(w.get("Neo"), "realm", Realm.MATRIX),
                                   setattr(w.get("Neo"), "power", max(w.get("Neo").power, 60))))

def ev_rescue_morpheus() -> Event:
    return Event(Movie.MATRIX, "Rescue Morpheus",
                 "Neo and Trinity rescue Morpheus from Agents.",
                 {Theme.LOVE_SACRIFICE, Theme.CONTROL_SYSTEMS}, [],
                 pre=lambda w: w.neo_awake and w.trinity_alive,
                 effect=lambda w: (setattr(w.get("Neo"), "power", max(w.get("Neo").power, 70)),
                                   setattr(w, "matrix_control", _clamp01(w.matrix_control - 0.03))))

def ev_neo_ascends() -> Event:
    def effect(w: World):
        neo = w.get("Neo")
        neo.power = max(neo.power, 90)
        w.matrix_control = _clamp01(w.matrix_control - 0.05)
        w.smith_factor = max(w.smith_factor, 0.05)
    return Event(Movie.MATRIX, "Ascension: stop bullets & fly",
                 "Neo sees the code; Agent Smith becomes a free anomaly.",
                 {Theme.MESSIANIC_GNOSIS, Theme.REALITY_ILLUSION, Theme.SMITH_SHADOW},
                 ["Messiah motif"], pre=lambda w: w.neo_awake, effect=effect)

def ev_merovingian_persephone() -> Event:
    return Event(Movie.RELOADED, "Merovingian & Persephone",
                 "Persephone's 'truth kiss' opens access to the Keymaker.",
                 {Theme.UNDERWORLD_PASSAGES, Theme.CONTROL_SYSTEMS},
                 ["Persephone (Underworld queen)"])

def ev_keymaker_freed() -> Event:
    return Event(Movie.RELOADED, "Keymaker freed",
                 "Backdoors to system internals become accessible.",
                 {Theme.CONTROL_SYSTEMS},
                 ["Janus (doors/thresholds)"],
                 effect=lambda w: setattr(w, "matrix_control", _clamp01(w.matrix_control - 0.04)))

def ev_architect_choice(choice: str) -> Event:
    def effect(w: World):
        if choice.upper() == "ZION":
            w.zion_defense = 1.0
            w.matrix_control = 1.0
            w.prophecy_valid = True
        else:
            w.prophecy_valid = False
            w.matrix_control = _clamp01(w.matrix_control - 0.02)
    return Event(Movie.RELOADED, "The Architect (choice)",
                 f"Neo chooses {'TRINITY (break cycle)' if choice.upper()!='ZION' else 'ZION (reset loop)'}",
                 {Theme.FREE_WILL, Theme.DETERMINISM, Theme.CONTROL_SYSTEMS},
                 ["Demiurge (Gnosis)"], effect=effect)

def ev_save_trinity() -> Event:
    return Event(Movie.RELOADED, "Save Trinity",
                 "Love over system logic; Trinity revived.",
                 {Theme.LOVE_SACRIFICE}, [],
                 pre=lambda w: w.trinity_alive,
                 effect=lambda w: setattr(w, "matrix_control", _clamp01(w.matrix_control - 0.02)))

def ev_smith_spreads(rate: float) -> Event:
    def effect(w: World):
        w.smith_factor = _clamp01(w.smith_factor + rate)
        w.matrix_control = _clamp01(w.matrix_control - 0.05)
    return Event(Movie.RELOADED, "Smith spreads",
                 "Smith replicates across programs and humans.",
                 {Theme.SMITH_SHADOW, Theme.CONTROL_SYSTEMS}, [],
                 effect=effect)

def ev_zion_assault(intensity: float) -> Event:
    def effect(w: World):
        w.zion_defense = _clamp01(w.zion_defense - intensity)
        w.zion_alive = w.zion_defense > 0.0
    return Event(Movie.REVOLUTIONS, "Sentinel assault on Zion",
                 "Sentinels erode Zion's defenses; docks under siege.",
                 {Theme.CONTROL_SYSTEMS}, [], effect=effect)

def ev_smith_copies_oracle() -> Event:
    def effect(w: World):
        w.smith_factor = _clamp01(w.smith_factor + 0.25)
    return Event(Movie.REVOLUTIONS, "Smith copies the Oracle",
                 "Smith gains 'sight' yet grows unstable.",
                 {Theme.SMITH_SHADOW}, ["Seer/Oracle"], effect=effect)

def ev_machines_negotiate() -> Event:
    return Event(Movie.REVOLUTIONS, "Machines negotiate (Deus Ex Machina)",
                 "Neo offers: end Smith ⇄ ceasefire + choice for humans.",
                 {Theme.HUMAN_MACHINE_SYMBIOSIS, Theme.FREE_WILL},
                 ["Deus ex machina (theater)"])

def ev_final_fight(bonus: int) -> Event:
    def effect(w: World):
        neo = w.get("Neo")
        neo_power = max(neo.power, 90)
        threshold = int(60 + 40 * w.smith_factor)
        score = neo_power + bonus
        if score >= threshold:
            w.smith_factor = 0.0
            w.matrix_control = 0.5
            neo.alive = False
            w.neo_alive = False
        else:
            w.smith_factor = _clamp01(w.smith_factor + 0.2)
    return Event(Movie.REVOLUTIONS, "Final fight: Neo vs Smith",
                 "Neo sacrifices; backreaction deletes Smith (if power ≥ threshold).",
                 {Theme.LOVE_SACRIFICE, Theme.SMITH_SHADOW, Theme.MESSIANIC_GNOSIS},
                 [], effect=effect)

def ev_peace() -> Event:
    def effect(w: World):
        if w.smith_factor == 0.0:
            w.peace = True
    return Event(Movie.REVOLUTIONS, "Peace accord",
                 "Ceasefire: humans may leave the Matrix (if Smith is gone).",
                 {Theme.HUMAN_MACHINE_SYMBIOSIS, Theme.FREE_WILL}, [], effect=effect)

# Canon builder (used by timeline)
def build_events_trilogy(architect_choice: str, smith_rate: float, zion_intensity: float, final_bonus: int) -> list[Event]:
    return [
        ev_awaken_neo(),
        ev_train_neo(),
        ev_rescue_morpheus(),
        ev_neo_ascends(),
        ev_merovingian_persephone(),
        ev_keymaker_freed(),
        ev_architect_choice(architect_choice),
        ev_save_trinity(),
        ev_smith_spreads(smith_rate),
        ev_zion_assault(zion_intensity),
        ev_smith_copies_oracle(),
        ev_machines_negotiate(),
        ev_final_fight(final_bonus),
        ev_peace(),
    ]
