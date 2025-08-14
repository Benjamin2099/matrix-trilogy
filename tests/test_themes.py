from matrix_sim.movies import build_trilogy, SimulationConfig
from matrix_sim.simulate import TimelineSimulator

def test_events_have_themes_and_myth_refs():
    world, events = build_trilogy(SimulationConfig())
    res = TimelineSimulator(world).run(events)
    # Prüfe, dass mindestens ein Event philosophische Themes trägt
    themed = [rec for rec in res.log if rec.get("themes")]
    assert themed, "No themed events found"
    # Beispiel: Architect-Event sollte FREE_WILL/DETERMINISM beinhalten
    architect = next(rec for rec in res.log if rec["event"].startswith("The Architect"))
    tset = set(architect.get("themes", []))
    assert "FREE_WILL" in tset and "DETERMINISM" in tset
