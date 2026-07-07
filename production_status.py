from dataclasses import dataclass
from typing import List

from project import Project
from scene import Scene


@dataclass
class SceneProductionStatus:
    scene_number: int
    has_prompt: bool
    has_rendered_video: bool
    has_edit_decision: bool
    has_continuity_metadata: bool
    ready_for_render: bool
    ready_for_edit: bool


@dataclass
class ProjectProductionStatus:
    total_scenes: int
    prompted_scenes: int
    rendered_scenes: int
    edit_ready_scenes: int
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

        return SceneProductionStatus(
            scene_number=scene.scene_number,
            has_prompt=has_prompt,
            has_rendered_video=has_rendered_video,
            has_edit_decision=has_edit_decision,
            has_continuity_metadata=bool(scene.continuity_metadata),
            ready_for_render=has_prompt,
            ready_for_edit=has_rendered_video and has_edit_decision,
        )