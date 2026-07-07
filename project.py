from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Project:
    title: str
    project_type: str
    source_text: str
    style: str
    inputs: List[str] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)
