from project import Project
from base_renderer import BaseRenderer
from render_types import RenderResult, RenderSettings
from scene import Scene


class FutureRenderer(BaseRenderer):
    """Placeholder for future renderer plugins."""

    name = "future"

    def render_scene(
        self,
        project: Project,
        scene: Scene,
        settings: RenderSettings,
    ) -> RenderResult:
        raise NotImplementedError("FutureRenderer is a plugin placeholder.")
