import json
from pathlib import Path
from typing import Any, Dict, List

from character import Character, CharacterRegistry
from edit_decision import EditDecision
from project import Project
from scene import Scene
from timeline import Timeline, TimelineEntry


class ProjectLoader:
    """Rebuilds a Project from Ghost Director's exported JSON manifest."""

    @staticmethod
    def load(path: str = "output/projects/project.json") -> Project:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        scenes = ProjectLoader._scenes(data.get("scenes", []))

        project = Project(
            title=data["title"],
            project_type=data["project_type"],
            source_text=data["source_text"],
            style=data["style"],
            inputs=data.get("inputs", []),
            metadata=data.get("metadata", {}),
            scenes=scenes,
            timeline=ProjectLoader._timeline(data.get("timeline", {}), scenes),
            character_registry=ProjectLoader._character_registry(
                data.get("character_registry", {}),
            ),
            assets=data.get("assets", {}),
            edit_decisions=ProjectLoader._edit_decisions(
                data.get("edit_decisions", []),
            ),
            rendered_video=data.get("rendered_video"),
        )

        return project

    @staticmethod
    def _scenes(items: List[Dict[str, Any]]) -> List[Scene]:
        return [ProjectLoader._scene(item) for item in items]

    @staticmethod
    def _scene(data: Dict[str, Any]) -> Scene:
        scene_data = dict(data)
        scene_data["characters"] = [
            Character(**character)
            for character in scene_data.get("characters", [])
        ]

        return Scene(**scene_data)

    @staticmethod
    def _timeline(data: Dict[str, Any], scenes: List[Scene]) -> Timeline:
        entries = [
            TimelineEntry(
                scene_number=entry["scene_number"],
                start_time=entry["start_time"],
                duration=entry["duration"],
                transition=entry.get("transition", "cut"),
                overlap=entry.get("overlap", 0.0),
            )
            for entry in data.get("entries", [])
        ]

        return Timeline(scenes=scenes, entries=entries)

    @staticmethod
    def _character_registry(data: Dict[str, Any]) -> CharacterRegistry:
        characters = {
            character_id: Character(**character)
            for character_id, character in data.get("characters", {}).items()
        }

        return CharacterRegistry(
            characters=characters,
            source_ids=data.get("source_ids", {}),
        )

    @staticmethod
    def _edit_decisions(items: List[Dict[str, Any]]) -> List[EditDecision]:
        return [
            EditDecision(
                scene_number=item["scene_number"],
                video_path=item["video_path"],
                start_time=item["start_time"],
                end_time=item["end_time"],
                duration=item["duration"],
                transition=item.get("transition", "cut"),
            )
            for item in items
        ]
