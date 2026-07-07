import json
from pathlib import Path
from typing import Dict


class WorkflowLoader:
    def __init__(self, workflow_path: str = "workflows/seedance.json"):
        self.workflow_path = Path(workflow_path)

    def load(self) -> Dict:
        with self.workflow_path.open("r", encoding="utf-8") as file:
            return json.load(file)
