import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Dict, Optional


class WorkflowValidationError(RuntimeError):
    """Raised when a renderer workflow cannot be used safely."""


class WorkflowFileMissingError(WorkflowValidationError):
    """Raised when the configured workflow file does not exist."""


class WorkflowJsonError(WorkflowValidationError):
    """Raised when the workflow file is not valid JSON."""


class WorkflowStructureError(WorkflowValidationError):
    """Raised when the workflow JSON is missing required renderer nodes."""


class WorkflowValidator:
    """Validates workflow files before anything is submitted to a renderer."""

    def validate_file(self, workflow_path: Path) -> Dict[str, Any]:
        if not workflow_path.exists():
            raise WorkflowFileMissingError(
                f"Workflow file does not exist: {workflow_path}"
            )

        try:
            with workflow_path.open("r", encoding="utf-8") as file:
                workflow = json.load(file)
        except JSONDecodeError as exc:
            raise WorkflowJsonError(
                f"Workflow file is not valid JSON: {workflow_path}"
            ) from exc

        self.validate_workflow(workflow, workflow_path)
        return workflow

    def validate_workflow(
        self,
        workflow: Dict[str, Any],
        workflow_path: Optional[Path] = None,
    ) -> None:
        location = f" in {workflow_path}" if workflow_path else ""

        if not isinstance(workflow, dict):
            raise WorkflowStructureError(
                f"Workflow JSON{location} must be an object."
            )

        if not workflow:
            raise WorkflowStructureError(
                f"Workflow JSON{location} is empty."
            )

        if not self._has_node(workflow):
            raise WorkflowStructureError(
                f"Workflow JSON{location} does not contain any renderer nodes."
            )

        if self.find_prompt_node(workflow) is None:
            raise WorkflowStructureError(
                f"Workflow JSON{location} is missing a prompt injection node."
            )

        if self.find_output_node(workflow) is None:
            raise WorkflowStructureError(
                f"Workflow JSON{location} is missing an output node."
            )

    def find_prompt_node(self, workflow: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self._find_node(workflow, self._is_prompt_node)

    def find_output_node(self, workflow: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self._find_node(workflow, self._is_output_node)

    def _has_node(self, value: Any) -> bool:
        return self._find_node(value, self._is_renderer_node) is not None

    def _find_node(self, value: Any, predicate) -> Optional[Dict[str, Any]]:
        if isinstance(value, dict):
            if predicate(value):
                return value

            for nested_value in value.values():
                result = self._find_node(nested_value, predicate)
                if result is not None:
                    return result

        if isinstance(value, list):
            for item in value:
                result = self._find_node(item, predicate)
                if result is not None:
                    return result

        return None

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

    def _is_output_node(self, node: Dict[str, Any]) -> bool:
        class_type = str(node.get("class_type", "")).lower()
        output_words = ["save", "output", "video", "vhs", "combine"]

        return any(word in class_type for word in output_words)
