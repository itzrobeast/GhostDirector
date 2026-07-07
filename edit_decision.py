from dataclasses import dataclass


@dataclass
class EditDecision:
    scene_number: int
    video_path: str
    start_time: float
    end_time: float
    duration: float
    transition: str = "cut"
