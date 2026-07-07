from typing import Optional

from comfy_client import ComfyClient
from project import Project
from workflow import WorkflowLoader
from workflow_builder import WorkflowBuilder


class Renderer:
    def __init__(self):
        self.workflow_loader = WorkflowLoader()
        self.workflow_builder = WorkflowBuilder()
        self.comfy_client = ComfyClient()

    def render(self, project: Project) -> Optional[str]:
        workflow = self.workflow_loader.load()
        print("Loaded Seedance workflow successfully.")

        for scene in project.scenes[:1]:
            print(f"Rendering Scene {scene.scene_number:03d}")
            scene_workflow = self.workflow_builder.build(workflow, scene)
            print(f"Workflow built for Scene {scene.scene_number:03d}.")
            video_path = self.comfy_client.render(scene_workflow)
            print(f"Scene {scene.scene_number:03d} rendered successfully.")
            return video_path

        return None
