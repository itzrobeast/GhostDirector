from dataclasses import dataclass, field
from typing import List, Optional

from scene import Scene


@dataclass
class TimelineEntry:
    scene_number: int
    start_time: float
    duration: float
    transition: str = "cut"
    overlap: float = 0.0

    @property
    def end_time(self) -> float:
        return self.start_time + self.duration


@dataclass
class Timeline:
    scenes: List[Scene] = field(default_factory=list)
    entries: List[TimelineEntry] = field(default_factory=list)

    @classmethod
    def from_scenes(cls, scenes: List[Scene]) -> "Timeline":
        timeline = cls(scenes=list(scenes))
        timeline.entries = [
            TimelineEntry(
                scene_number=scene.scene_number,
                start_time=scene.start_time,
                duration=scene.duration,
            )
            for scene in scenes
        ]
        return timeline

    def next_scene(self, scene: Scene) -> Optional[Scene]:
        index = self._index(scene)
        if index is None or index + 1 >= len(self.scenes):
            return None

        return self.scenes[index + 1]

    def previous_scene(self, scene: Scene) -> Optional[Scene]:
        index = self._index(scene)
        if index is None or index == 0:
            return None

        return self.scenes[index - 1]

    def total_duration(self) -> float:
        if not self.entries:
            return 0.0

        return max(entry.end_time for entry in self.entries)

    def _index(self, scene: Scene) -> Optional[int]:
        for index, timeline_scene in enumerate(self.scenes):
            if timeline_scene.scene_number == scene.scene_number:
                return index

        return None
