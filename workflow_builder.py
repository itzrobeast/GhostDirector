from copy import deepcopy
from typing import Any, Dict, Optional

from scene import Scene


class WorkflowBuilder:
    def build(
        self,
        workflow: Dict[str, Any],
        scene: Scene,
    ) -> Dict[str, Any]:
        scene_workflow = deepcopy(workflow)
        prompt_node = self._find_prompt_node(scene_workflow)

        if prompt_node is not None:
            inputs = prompt_node.setdefault("inputs", {})
            prompt_key = self._prompt_key(inputs)
            inputs[prompt_key] = scene.prompt

        return scene_workflow

    def _find_prompt_node(self, workflow: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for value in workflow.values():
            if isinstance(value, dict) and self._is_prompt_node(value):
                return value

        return self._find_nested_prompt_node(workflow)

    def _find_nested_prompt_node(self, value: Any) -> Optional[Dict[str, Any]]:
        if isinstance(value, dict):
            if self._is_prompt_node(value):
                return value

            for nested_value in value.values():
                result = self._find_nested_prompt_node(nested_value)
                if result is not None:
                    return result

        if isinstance(value, list):
            for item in value:
                result = self._find_nested_prompt_node(item)
                if result is not None:
                    return result

        return None

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
