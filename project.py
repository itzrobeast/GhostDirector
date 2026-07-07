from dataclasses import dataclass, field
from typing import Dict, List, Optional

from character import CharacterRegistry
from edit_decision import EditDecision
from scene import Scene
from timeline import Timeline


@dataclass
class Project:
    title: str
    project_type: str
    source_text: str
    style: str
    inputs: List[str] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)
    scenes: List[Scene] = field(default_factory=list)
    timeline: Timeline = field(default_factory=Timeline)
    character_registry: CharacterRegistry = field(default_factory=CharacterRegistry)
    assets: Dict[str, str] = field(default_factory=dict)
    edit_decisions: List[EditDecision] = field(default_factory=list)
    rendered_video: Optional[str] = None
