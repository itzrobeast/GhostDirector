from typing import Optional

from asset_manager import AssetManager
from base_renderer import BaseRenderer
from comfy_client import ComfyClient
from project import Project
from render_types import RenderResult, RenderSettings
from scene import Scene
from workflow import WorkflowLoader
from workflow_builder import WorkflowBuilder


class ComfyRenderer(BaseRenderer):
    """ComfyUI renderer plugin implementation."""

    name = "comfy"

    def __init__(
        self,
        asset_manager: Optional[AssetManager] = None,
        workflow_loader: Optional[WorkflowLoader] = None,
        workflow_builder: Optional[WorkflowBuilder] = None,
        comfy_client: Optional[ComfyClient] = None,
    ):
        self.asset_manager = asset_manager or AssetManager()
        self.workflow_loader = workflow_loader or WorkflowLoader()
        self.workflow_builder = workflow_builder or WorkflowBuilder()
        self.comfy_client = comfy_client or ComfyClient()

    def render_scene(
        self,
        project: Project,
        scene: Scene,
        settings: RenderSettings,
    ) -> RenderResult:
        workflow = self.workflow_loader.load()
        scene_workflow = self.workflow_builder.build(workflow, scene, settings)
        video_path = self.comfy_client.render(scene_workflow)

        return RenderResult(
            scene_number=scene.scene_number,
            video_path=video_path or settings.output_filename,
            status="finished",
            diagnostics=["ComfyUI render completed."],
        )


class SeedanceRenderer(ComfyRenderer):
    """Seedance renderer backed by a ComfyUI workflow."""

    name = "seedance"
