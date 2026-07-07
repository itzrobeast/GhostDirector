from project import Project


class Renderer:
    def render(self, project: Project) -> None:
        for scene in project.scenes:
            print(f"Rendering Scene {scene.scene_number:03d}")
