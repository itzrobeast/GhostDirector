from abc import ABC, abstractmethod

from project import Project
from render_types import RenderResult, RenderSettings
from scene import Scene


class BaseRenderer(ABC):
    """Renderer plugin interface for converting scenes into media."""

    name = "base"

    @abstractmethod
    def render_scene(
        self,
        project: Project,
        scene: Scene,
        settings: RenderSettings,
    ) -> RenderResult:
        raise NotImplementedError
