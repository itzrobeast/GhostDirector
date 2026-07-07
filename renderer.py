from project import Project
from workflow import WorkflowLoader


class Renderer:
    def __init__(self):
        self.workflow_loader = WorkflowLoader()

    def render(self, project: Project) -> None:
        self.workflow_loader.load()
        print("Loaded Seedance workflow successfully.")

        for scene in project.scenes:
            print(f"Rendering Scene {scene.scene_number:03d}")
