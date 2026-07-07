from dataclasses import dataclass, field
from typing import Dict, List, Optional
from uuid import UUID, uuid4


@dataclass
class Character:
    id: str
    name: str = ""
    description: str = ""
    age: Optional[int] = None
    gender: Optional[str] = None
    species: str = "human"
    appearance: str = ""
    hair: str = ""
    skin: str = ""
    eyes: str = ""
    clothing: str = ""
    voice: str = ""
    accessories: List[str] = field(default_factory=list)
    personality: str = ""
    hairstyle: str = ""
    facial_expression: str = ""
    emotional_state: str = ""
    current_location: str = ""
    props: List[str] = field(default_factory=list)


@dataclass
class CharacterRegistry:
    characters: Dict[str, Character] = field(default_factory=dict)
    source_ids: Dict[str, str] = field(default_factory=dict)

    def register(self, character: Character) -> Character:
        character.id = self._registry_id(character.id)

        existing = self.characters.get(character.id)
        if existing:
            self._update(existing, character)
            return existing

        self.characters[character.id] = character
        return character

    def get(self, character_id: str) -> Optional[Character]:
        return self.characters.get(character_id)

    def all(self) -> List[Character]:
        return list(self.characters.values())

    def _registry_id(self, source_id: str) -> str:
        if self._is_uuid(source_id):
            return source_id

        if source_id and source_id not in self.source_ids:
            self.source_ids[source_id] = self._new_id()

        if source_id:
            return self.source_ids[source_id]

        return self._new_id()

    def _new_id(self) -> str:
        return str(uuid4())

    def _is_uuid(self, value: str) -> bool:
        if not value:
            return False

        try:
            UUID(value)
        except ValueError:
            return False

        return True

    def _update(self, existing: Character, incoming: Character) -> None:
        for field_name, value in incoming.__dict__.items():
            if value:
                setattr(existing, field_name, value)
