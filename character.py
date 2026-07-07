from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Character:
    id: str
    name: str = ""
    description: str = ""
    age: Optional[int] = None
    gender: Optional[str] = None
    species: str = "human"
    clothing: str = ""
    hairstyle: str = ""
    accessories: List[str] = field(default_factory=list)
    facial_expression: str = ""
    emotional_state: str = ""
    current_location: str = ""
    props: List[str] = field(default_factory=list)
