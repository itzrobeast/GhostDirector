from dataclasses import dataclass
from typing import List

from project import Project
from render_status import COMPLETE, FAILED, NOT_STARTED, WAITING
from scene import Scene


@dataclass
class SceneProductionStatus:
    scene_number: int
    status: str
    has_prompt: bool
    has_rendered_video: bool
    has_edit_decision: bool
    has_continuity_metadata: bool
    ready_for_render: bool
    ready_for_edit: bool
    progress: float = 0.0
    error: str = ""


@dataclass
class ProjectProductionStatus:
    total_scenes: int
    prompted_scenes: int
    rendered_scenes: int
    edit_ready_scenes: int
    failed_scenes: int
    status: str
    scenes: List[SceneProductionStatus]


class ProductionStatus:
    """Reports where a project is in the film production pipeline."""

    def review(self, project: Project) -> ProjectProductionStatus:
        edit_scene_numbers = {
            decision.scene_number for decision in project.edit_decisions
        }
        scene_statuses = [
            self._scene_status(scene, edit_scene_numbers)
            for scene in project.scenes
        ]

        return ProjectProductionStatus(
            total_scenes=len(scene_statuses),
            prompted_scenes=sum(
                1 for status in scene_statuses if status.has_prompt
            ),
            rendered_scenes=sum(
                1 for status in scene_statuses if status.has_rendered_video
            ),
            edit_ready_scenes=sum(
                1 for status in scene_statuses if status.ready_for_edit
            ),
            failed_scenes=sum(
                1 for status in scene_statuses if status.status == FAILED
            ),
            status=self._project_status(scene_statuses),
            scenes=scene_statuses,
        )

    def _scene_status(
        self,
        scene: Scene,
        edit_scene_numbers: set[int],
    ) -> SceneProductionStatus:
        has_prompt = bool(scene.prompt)
        has_rendered_video = bool(scene.rendered_video)
        has_edit_decision = scene.scene_number in edit_scene_numbers
        status = self._status(scene, has_prompt, has_rendered_video)

        return SceneProductionStatus(
            scene_number=scene.scene_number,
            status=status,
            has_prompt=has_prompt,
            has_rendered_video=has_rendered_video,
            has_edit_decision=has_edit_decision,
            has_continuity_metadata=bool(scene.continuity_metadata),
            ready_for_render=has_prompt and not has_rendered_video,
            ready_for_edit=has_rendered_video and has_edit_decision,
            progress=scene.render_progress,
            error=scene.render_error,
        )

    def _status(
        self,
        scene: Scene,
        has_prompt: bool,
        has_rendered_video: bool,
    ) -> str:
        if has_rendered_video:
            return COMPLETE

        if scene.render_status != NOT_STARTED:
            return scene.render_status

        if has_prompt:
            return WAITING

        return NOT_STARTED

    def _project_status(self, scenes: List[SceneProductionStatus]) -> str:
        if not scenes:
            return NOT_STARTED

        if any(scene.status == FAILED for scene in scenes):
            return FAILED

        if all(scene.status == COMPLETE for scene in scenes):
            return COMPLETE

        if any(scene.status != NOT_STARTED for scene in scenes):
            return WAITING

        return NOT_STARTED
