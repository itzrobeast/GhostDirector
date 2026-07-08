from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RenderSettings:
    width: int = 1280
    height: int = 720
    duration: float = 5.0
    fps: int = 24
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
