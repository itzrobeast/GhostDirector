from dataclasses import dataclass
from typing import List, Optional

from project import Project
from scene import Scene


@dataclass
class RenderQueueItem:
    scene_number: int
    reason: str


class RenderQueue:
    """Selects scenes that are prompted and still need rendering."""

    def build(
        self,
        project: Project,
        scene_numbers: Optional[List[int]] = None,
    ) -> List[RenderQueueItem]:
        selected_numbers = set(scene_numbers or [])
        items = []

        for scene in project.scenes:
            if selected_numbers and scene.scene_number not in selected_numbers:
                continue

            if self._ready_for_render(scene):
                items.append(
                    RenderQueueItem(
                        scene_number=scene.scene_number,
                        reason="Prompt exists and no rendered video is assigned.",
                    )
                )

        return items

    def _ready_for_render(self, scene: Scene) -> bool:
        return bool(scene.prompt) and not bool(scene.rendered_video)