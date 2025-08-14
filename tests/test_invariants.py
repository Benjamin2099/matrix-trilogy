from matrix_sim.movies import build_trilogy, SimulationConfig
from matrix_sim.simulate import TimelineSimulator

def run(cfg: SimulationConfig):
    world, events = build_trilogy(cfg)
    result = TimelineSimulator(world).run(events)
    return result

def test_peace_requires_smith_zero():
    # Canon: Smith wird gelöscht -> Frieden True
    r = run(SimulationConfig(architect_choice="TRINITY", smith_rate=0.3, zion_intensity=0.25, final_bonus=8))
    final = r.log[-1]["snapshot"]
    assert final["peace"] is True
    assert final["smith_factor"] == 0.0

def test_architect_zion_resets_system():
    # Alternativpfad: ZION (klassischer Reset)
    r = run(SimulationConfig(architect_choice="ZION", smith_rate=0.15, zion_intensity=0.15, final_bonus=6))
    # Finde den Architect-Log
    arch_logs = [rec for rec in r.log if rec["event"].startswith("The Architect")]
    assert arch_logs, "Architect event missing"
    # Nach Architect sollte prophecy_valid True und matrix_control evtl. hoch sein (Reset)
    # Wir prüfen am Snapshot genau dieses Events:
    snap = arch_logs[0]["snapshot"]
    assert snap["prophecy_valid"] is True
    assert snap["matrix_control"] >= 0.99  # Reset auf 1.0 im Code

def test_zion_assault_reduces_defense():
    r = run(SimulationConfig())
    # Finde den ersten Zion-Angriff
    assault = next(rec for rec in r.log if "Sentinel assault" in rec["event"])
    before = 0.4  # default start
    after = assault["snapshot"]["zion_defense"]
    assert after < before
