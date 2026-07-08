from pathlib import Path
from typing import Any, Dict

from workflow_validation import WorkflowValidator


class WorkflowLoader:
    def __init__(self, workflow_path: str = "workflows/seedance.json"):
        self.workflow_path = Path(workflow_path)
        self.validator = WorkflowValidator()

    def load(self) -> Dict[str, Any]:
        return self.validator.validate_file(self.workflow_path)
