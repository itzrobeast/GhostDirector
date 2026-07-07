from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from character import Character


@dataclass
class Scene:
    scene_number: int

    # Timing
    start_time: float
    duration: float

    # Source
    lyrics: str

    # Story
    scene_type: str
    emotion: str
    energy: str

    # Visuals
    location: str
    lighting: str
    weather: str
    time_of_day: str

    # Camera
    camera: str
    lens: str
    movement: str
    camera_language: Dict[str, str] = field(default_factory=dict)

    # Character
    action: str
    expression: str

    # Continuity
    continuity: bool
    use_last_frame: bool

    # Creative Metadata
    environment: str = ""
    mood: str = ""
    dominant_color_palette: str = ""
    continuity_notes: str = ""
    continuity_metadata: Dict[str, Any] = field(default_factory=dict)
    character_ids: List[str] = field(default_factory=list)
    characters: List[Character] = field(default_factory=list)

    # Final Output
    prompt: str = ""
    rendered_video: Optional[str] = None
