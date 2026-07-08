from dataclasses import dataclass
from typing import List, Optional

from project import Project
from render_status import COMPLETE, FAILED, QUEUED, RETRY, WAITING
from scene import Scene


@dataclass
class RenderQueueItem:
    scene_number: int
    status: str
    reason: str
    progress: float = 0.0
    estimated_render_seconds: Optional[int] = None
    attempts: int = 0
    depends_on: Optional[List[int]] = None

    def __post_init__(self) -> None:
        if self.depends_on is None:
            self.depends_on = []


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

            item = self._queue_item(scene)
            if item is not None:
                items.append(item)

        return items

    def _queue_item(self, scene: Scene) -> Optional[RenderQueueItem]:
        if scene.render_status == COMPLETE or scene.rendered_video:
            return None

        if not scene.prompt:
            return RenderQueueItem(
                scene_number=scene.scene_number,
                status=WAITING,
                reason="Scene is waiting for a prompt before rendering.",
                progress=scene.render_progress,
                estimated_render_seconds=scene.estimated_render_seconds,
                attempts=scene.render_attempts,
            )

        status = scene.render_status
        reason = "Prompt exists and no rendered video is assigned."

        if scene.render_status == FAILED:
            status = RETRY
            reason = "Previous render failed and can be retried."
        elif scene.render_status in [WAITING, QUEUED]:
            status = scene.render_status
        else:
            status = QUEUED

        return RenderQueueItem(
            scene_number=scene.scene_number,
            status=status,
            reason=reason,
            progress=scene.render_progress,
            estimated_render_seconds=scene.estimated_render_seconds,
            attempts=scene.render_attempts,
        )
