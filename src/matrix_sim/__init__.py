
## `src/matrix_sim/__init__.py`
from .engine import World, Character, Faction, Realm, Movie, Theme
from .events import Event, build_events_trilogy, ev_smith_spreads, ev_zion_assault
from .movies import SimulationConfig, build_trilogy
from .simulate import TimelineSimulator, format_timeline
from .agents import AgentSimulator, NeoAgent, SmithAgent, MachineCollectiveAgent
