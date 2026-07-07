from comfy_client import ComfyClient
from project import Project
from workflow import WorkflowLoader
from workflow_builder import WorkflowBuilder


class Renderer:
    def __init__(self):
        self.workflow_loader = WorkflowLoader()
        self.workflow_builder = WorkflowBuilder()
        self.comfy_client = ComfyClient()

    def render(self, project: Project) -> None:
        workflow = self.workflow_loader.load()
        print("Loaded Seedance workflow successfully.")

        for scene in project.scenes[:1]:
            print(f"Rendering Scene {scene.scene_number:03d}")
            scene_workflow = self.workflow_builder.build(workflow, scene)
            print(f"Workflow built for Scene {scene.scene_number:03d}.")
            self.comfy_client.submit(scene_workflow)
