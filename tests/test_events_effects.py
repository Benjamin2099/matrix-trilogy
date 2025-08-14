from matrix_sim.movies import build_trilogy, SimulationConfig
from matrix_sim.simulate import TimelineSimulator

def test_smith_spreads_increases_factor():
    r = TimelineSimulator(build_trilogy(SimulationConfig(smith_rate=0.5))[0]).run(
        build_trilogy(SimulationConfig(smith_rate=0.5))[1]
    )
    recs = [rec for rec in r.log if rec["event"].startswith("Smith spreads")]
    assert recs, "Smith spreads event missing"
    # Prüfen: smith_factor nach Spread > 0
    assert recs[-1]["snapshot"]["smith_factor"] >= 0.5

def test_final_fight_eliminates_smith_and_kills_neo_in_canon():
    # final_bonus ausreichend hoch -> Smith wird gelöscht, Neo stirbt (kanonischer Pfad)
    cfg = SimulationConfig(architect_choice="TRINITY", smith_rate=0.3, zion_intensity=0.25, final_bonus=8)
    world, events = build_trilogy(cfg)
    result = TimelineSimulator(world).run(events)
    snap = result.log[-2]["snapshot"]  # vor "End" kommt "Peace accord" – wir wollen den Stand nach dem Final Fight o. Peace
    assert snap["smith_factor"] == 0.0
    assert snap["neo_alive"] is False
