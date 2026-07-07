from typing import Optional

from asset_manager import AssetManager
from comfy_client import ComfyClient
from project import Project
from workflow import WorkflowLoader
from workflow_builder import WorkflowBuilder


class Renderer:
    def __init__(self, asset_manager: Optional[AssetManager] = None):
        self.asset_manager = asset_manager or AssetManager()
        self.workflow_loader = WorkflowLoader()
        self.workflow_builder = WorkflowBuilder()
        self.comfy_client = ComfyClient()

    def render(self, project: Project) -> Optional[str]:
        workflow = self.workflow_loader.load()
        print("Loaded Seedance workflow successfully.")

        for scene in project.scenes[:1]:
            print(f"Rendering Scene {scene.scene_number:03d}")
            managed_video = self.asset_manager.get_scene_video(scene.scene_number)
            scene_workflow = self.workflow_builder.build(workflow, scene)
            print(f"Workflow built for Scene {scene.scene_number:03d}.")
            video_path = self.comfy_client.render(scene_workflow)
            scene.rendered_video = video_path or str(managed_video)
            print(f"Scene {scene.scene_number:03d} rendered successfully.")
            return scene.rendered_video

        return None
