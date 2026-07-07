from dataclasses import dataclass, field
from typing import Dict, List, Optional

from character import CharacterRegistry
from scene import Scene


@dataclass
class Project:
    title: str
    project_type: str
    source_text: str
    style: str
    inputs: List[str] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)
    scenes: List[Scene] = field(default_factory=list)
    character_registry: CharacterRegistry = field(default_factory=CharacterRegistry)
    rendered_video: Optional[str] = None
