from __future__ import annotations
import argparse, sys, random, json
from .movies import build_trilogy, SimulationConfig
from .simulate import TimelineSimulator, format_timeline
from .agents import AgentSimulator, NeoAgent, SmithAgent, MachineCollectiveAgent

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Matrix Trilogy Simulation (timeline + agents)")
    p.add_argument("--mode", choices=["timeline","agent"], default="timeline")
    p.add_argument("--scenario", choices=["canon","zion_falls","neo_chooses_zion"], default="canon")
    p.add_argument("--architect", choices=["TRINITY","ZION"], default=None)
    p.add_argument("--smith-rate", type=float, default=None)
    p.add_argument("--zion-intensity", type=float, default=None)
    p.add_argument("--final-bonus", type=int, default=None)
    p.add_argument("--jsonl", type=str, default=None)
    p.add_argument("--ticks", type=int, default=12)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--print-report", action="store_true", help="Print theme coverage & final snapshot")
    p.add_argument("--query-theme", type=str, default=None, help="Filter events by theme name")
    args = p.parse_args(argv)

    # Presets
    if args.scenario == "canon":
        cfg = SimulationConfig("TRINITY", 0.30, 0.25, 8)
    elif args.scenario == "zion_falls":
        cfg = SimulationConfig("TRINITY", 0.45, 0.40, 6)
    else:
        cfg = SimulationConfig("ZION", 0.15, 0.15, 6)

    # Overrides
    if args.architect: cfg.architect_choice = args.architect
    if args.smith_rate is not None: cfg.smith_rate = args.smith_rate
    if args.zion_intensity is not None: cfg.zion_intensity = args.zion_intensity
    if args.final_bonus is not None: cfg.final_bonus = args.final_bonus

    world, events = build_trilogy(cfg)

    if args.mode == "timeline":
        sim = TimelineSimulator(world, jsonl_path=args.jsonl)
        result = sim.run(events)
        print(format_timeline(result.log))
        if args.print_report or args.query_theme:
            _maybe_report_and_query(result.log, args.query_theme)
        return 0

    # agent mode
    rng = random.Random(args.seed)
    agents = [NeoAgent("NeoAgent", rng), SmithAgent("SmithAgent", rng), MachineCollectiveAgent("MachineAgent", rng)]
    agent_sim = AgentSimulator(world, rng, max_ticks=args.ticks)
    result = agent_sim.run(agents)
    print(format_timeline(result.log))
    if args.print_report or args.query_theme:
        _maybe_report_and_query(result.log, args.query_theme)
    return 0

def _maybe_report_and_query(log, theme_name):
    counts = {}
    for rec in log:
        for t in rec.get("themes", []):
            counts[t] = counts.get(t, 0) + 1
    print("\n=== Theme Coverage ===")
    print(json.dumps(dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))), indent=2))
    print("\n=== Final Snapshot ===")
    print(json.dumps(log[-1]["snapshot"], indent=2))
    if theme_name:
        theme_name = theme_name.strip().upper()
        print(f"\n=== Events with theme {theme_name} ===")
        for rec in log:
            if theme_name in rec.get("themes", []):
                print(f"{rec['movie']} :: {rec['event']} — {rec['desc']}")

if __name__ == "__main__":
    raise SystemExit(main())
