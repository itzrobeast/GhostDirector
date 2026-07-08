from pathlib import Path
from typing import Any, Dict, Optional

from config import DEFAULT_CONFIG
from structured_logger import logger
from workflow_validation import WorkflowValidator


class WorkflowLoader:
    def __init__(self, workflow_path: Optional[str] = None):
        self.workflow_path = Path(
            workflow_path or DEFAULT_CONFIG.workflow.seedance_path
        )
        self.validator = WorkflowValidator()

    def load(self) -> Dict[str, Any]:
        logger.info("workflow_loading", workflow_path=str(self.workflow_path))
        workflow = self.validator.validate_file(self.workflow_path)
        logger.info("workflow_loaded", workflow_path=str(self.workflow_path))
        return workflow
