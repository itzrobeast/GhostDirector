from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from character import Character
from render_status import NOT_STARTED


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
    camera_language: Dict[str, str] = field(default_factory=dict)
    continuity_notes: str = ""
    continuity_metadata: Dict[str, Any] = field(default_factory=dict)
    directorial_beats: Dict[str, str] = field(default_factory=dict)
    character_ids: List[str] = field(default_factory=list)
    characters: List[Character] = field(default_factory=list)

    # Rendering
    render_status: str = NOT_STARTED
    render_progress: float = 0.0
    render_error: str = ""
    render_attempts: int = 0
    estimated_render_seconds: Optional[int] = None

    # Final Output
    prompt_layers: Dict[str, str] = field(default_factory=dict)
    prompt: str = ""
    rendered_video: Optional[str] = None
