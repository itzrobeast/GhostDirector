from dataclasses import dataclass


@dataclass
class Shot:
    shot_number: int
    scene_number: int

    # Timing
    start_time: float
    duration: float

    # Story
    shot_type: str

    # Camera
    camera: str
    lens: str
    movement: str
    framing: str
    composition: str

    # Visuals
    location: str
    lighting: str
    weather: str
    time_of_day: str

    # Character
    action: str
    expression: str

    # Final Output
    prompt: str = ""
