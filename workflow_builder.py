from copy import deepcopy
from typing import Any, Dict, Optional

from render_types import RenderSettings
from scene import Scene


class WorkflowBuilder:
    def build(
        self,
        workflow: Dict[str, Any],
        scene: Scene,
        settings: Optional[RenderSettings] = None,
    ) -> Dict[str, Any]:
        scene_workflow = deepcopy(workflow)
        render_settings = settings or RenderSettings(duration=scene.duration)
        prompt_node = self._find_prompt_node(scene_workflow)

        if prompt_node is None:
            raise ValueError("Workflow is missing a prompt injection node.")

        self._inject_prompt(prompt_node, scene.prompt)
        self._inject_negative_prompt(scene_workflow, render_settings)
        self._inject_known_settings(scene_workflow, render_settings)
        self._inject_metadata(scene_workflow, scene, render_settings)

        return scene_workflow

    def _inject_prompt(self, prompt_node: Dict[str, Any], prompt: str) -> None:
        inputs = prompt_node.setdefault("inputs", {})
        prompt_key = self._prompt_key(inputs)
        inputs[prompt_key] = prompt

    def _inject_negative_prompt(
        self,
        workflow: Dict[str, Any],
        settings: RenderSettings,
    ) -> None:
        if not settings.negative_prompt:
            return

        for node in self._iter_nodes(workflow):
            inputs = node.get("inputs", {})
            class_type = str(node.get("class_type", "")).lower()
            if not isinstance(inputs, dict):
                continue

            if "negative" in class_type:
                key = self._prompt_key(inputs)
                inputs[key] = settings.negative_prompt
                return

            for key in ["negative", "negative_prompt"]:
                if key in inputs:
                    inputs[key] = settings.negative_prompt
                    return

    def _inject_known_settings(
        self,
        workflow: Dict[str, Any],
        settings: RenderSettings,
    ) -> None:
        replacements = {
            "seed": settings.seed,
            "width": settings.width,
            "height": settings.height,
            "duration": settings.duration,
            "fps": settings.fps,
            "frame_rate": settings.fps,
            "filename_prefix": settings.output_filename,
            "output_filename": settings.output_filename,
        }

        for node in self._iter_nodes(workflow):
            inputs = node.get("inputs", {})
            if not isinstance(inputs, dict):
                continue

            for key, value in replacements.items():
                if value is not None and value != "" and key in inputs:
                    inputs[key] = value

            self._inject_loras(inputs, settings)

    def _inject_loras(
        self,
        inputs: Dict[str, Any],
        settings: RenderSettings,
    ) -> None:
        if not settings.loras:
            return

        for key in list(inputs.keys()):
            lower_key = key.lower()
            if lower_key.endswith("_strength"):
                lora_name = lower_key.removesuffix("_strength")
                if lora_name in settings.loras:
                    inputs[key] = settings.loras[lora_name]

    def _inject_metadata(
        self,
        workflow: Dict[str, Any],
        scene: Scene,
        settings: RenderSettings,
    ) -> None:
        metadata = {
            "scene_number": scene.scene_number,
            "camera": scene.camera_language,
            "continuity": scene.continuity_metadata,
            **settings.metadata,
        }

        for node in self._iter_nodes(workflow):
            inputs = node.get("inputs", {})
            if not isinstance(inputs, dict):
                continue

            if "metadata" in inputs:
                inputs["metadata"] = metadata

            if "camera_metadata" in inputs:
                inputs["camera_metadata"] = scene.camera_language

            if "scene_metadata" in inputs:
                inputs["scene_metadata"] = metadata

    def _find_prompt_node(self, workflow: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for node in self._iter_nodes(workflow):
            if self._is_prompt_node(node):
                return node

        return None

    def _iter_nodes(self, value: Any):
        if isinstance(value, dict):
            if self._is_renderer_node(value):
                yield value

            for nested_value in value.values():
                yield from self._iter_nodes(nested_value)

        if isinstance(value, list):
            for item in value:
                yield from self._iter_nodes(item)

    def _is_renderer_node(self, node: Dict[str, Any]) -> bool:
        return isinstance(node.get("inputs"), dict) and "class_type" in node

    def _is_prompt_node(self, node: Dict[str, Any]) -> bool:
        inputs = node.get("inputs", {})
        class_type = str(node.get("class_type", "")).lower()

        if not isinstance(inputs, dict):
            return False

        has_prompt_input = "text" in inputs or "prompt" in inputs
        looks_like_text_node = (
            "text" in class_type
            or "prompt" in class_type
            or "cliptextencode" in class_type
        )

        return has_prompt_input and looks_like_text_node

    def _prompt_key(self, inputs: Dict[str, Any]) -> str:
        if "text" in inputs:
            return "text"

        return "prompt"
