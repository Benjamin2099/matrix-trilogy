from matrix_sim.movies import build_trilogy, SimulationConfig
from matrix_sim.simulate import TimelineSimulator

def test_timeline_runs():
    w, events = build_trilogy(SimulationConfig())
    sim = TimelineSimulator(w)
    r = sim.run(events)
    assert any("Matrix (1999)" in rec["movie"] for rec in r.log)
    assert any("Matrix Revolutions" in rec["movie"] for rec in r.log)
    assert r.log[-1]["event"] == "End"
