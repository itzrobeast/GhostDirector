from dataclasses import dataclass


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

    # Final Output
    prompt: str = ""