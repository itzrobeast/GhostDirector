from typing import List, Optional

from asset_manager import AssetManager
from base_renderer import BaseRenderer
from comfy_renderer import SeedanceRenderer
from project import Project
from render_status import COMPLETE, FAILED, RENDERING
from render_types import RenderSettings
from scene import Scene


class Renderer:
    """Coordinates scene rendering through an interchangeable renderer plugin."""

    def __init__(
        self,
        asset_manager: Optional[AssetManager] = None,
        backend: Optional[BaseRenderer] = None,
    ):
        self.asset_manager = asset_manager or AssetManager()
        self.backend = backend or SeedanceRenderer(self.asset_manager)

    def render(
        self,
        project: Project,
        scene_numbers: Optional[List[int]] = None,
    ) -> List[str]:
        rendered_videos = []

        for scene in self._selected_scenes(project, scene_numbers):
            print(f"Rendering Scene {scene.scene_number:03d}")
            print(f"Renderer: {self.backend.name}")
            print(f"Camera language: {scene.camera_language}")
            scene.render_status = RENDERING
            scene.render_progress = 0.0
            scene.render_error = ""
            scene.render_attempts += 1

            try:
                settings = self._settings_for_scene(scene)
                result = self.backend.render_scene(project, scene, settings)
                managed_video = self.asset_manager.normalize_scene_video(
                    scene.scene_number,
                    result.video_path,
                )
                scene.rendered_video = managed_video
                scene.render_status = COMPLETE
                scene.render_progress = 1.0
                rendered_videos.append(managed_video)
                print(f"Scene {scene.scene_number:03d} rendered successfully.")
            except Exception as exc:
                scene.render_status = FAILED
                scene.render_error = str(exc)
                scene.render_progress = 0.0
                raise

        return rendered_videos

    def _selected_scenes(
        self,
        project: Project,
        scene_numbers: Optional[List[int]],
    ) -> List[Scene]:
        if scene_numbers:
            selected_numbers = set(scene_numbers)
            return [
                scene
                for scene in project.scenes
                if scene.scene_number in selected_numbers
            ]

        return project.scenes[:1]

    def _settings_for_scene(self, scene: Scene) -> RenderSettings:
        return RenderSettings(
            duration=scene.duration,
            output_filename=str(
                self.asset_manager.get_scene_video(scene.scene_number)
            ),
            negative_prompt=scene.prompt_layers.get("negative_prompt", ""),
            metadata={
                "camera": scene.camera_language,
                "continuity": scene.continuity_metadata,
                "scene_number": scene.scene_number,
            },
        )
