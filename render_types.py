from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from config import DEFAULT_CONFIG


@dataclass
class RenderSettings:
    width: int = DEFAULT_CONFIG.render.width
    height: int = DEFAULT_CONFIG.render.height
    duration: float = DEFAULT_CONFIG.render.duration
    fps: int = DEFAULT_CONFIG.render.fps
    seed: Optional[int] = None
    output_filename: str = ""
    negative_prompt: str = ""
    loras: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RenderResult:
    scene_number: int
    video_path: str = ""
    prompt_id: str = ""
    status: str = "finished"
    diagnostics: List[str] = field(default_factory=list)
