from typing import List, Optional

from asset_manager import AssetManager
from comfy_client import ComfyClient
from project import Project
from scene import Scene
from workflow import WorkflowLoader
from workflow_builder import WorkflowBuilder


class Renderer:
    def __init__(self, asset_manager: Optional[AssetManager] = None):
        self.asset_manager = asset_manager or AssetManager()
        self.workflow_loader = WorkflowLoader()
        self.workflow_builder = WorkflowBuilder()
        self.comfy_client = ComfyClient()

    def render(
        self,
        project: Project,
        scene_numbers: Optional[List[int]] = None,
    ) -> List[str]:
        workflow = self.workflow_loader.load()
        print("Loaded Seedance workflow successfully.")
        rendered_videos = []

        for scene in self._selected_scenes(project, scene_numbers):
            print(f"Rendering Scene {scene.scene_number:03d}")
            print(f"Camera language: {scene.camera_language}")
            managed_video = self.asset_manager.get_scene_video(scene.scene_number)
            scene_workflow = self.workflow_builder.build(workflow, scene)
            print(f"Workflow built for Scene {scene.scene_number:03d}.")
            video_path = self.comfy_client.render(scene_workflow)
            scene.rendered_video = video_path or str(managed_video)
            rendered_videos.append(scene.rendered_video)
            print(f"Scene {scene.scene_number:03d} rendered successfully.")

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
