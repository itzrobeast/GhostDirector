import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from shutil import copytree, rmtree
from typing import Dict, List, Optional
from uuid import uuid4

from asset_manager import AssetManager
from asset_upload import safe_project_id
from project import Project


class ProjectStore:
    """Persists multiple Studio projects without changing the directing pipeline."""

    def __init__(self, asset_manager: Optional[AssetManager] = None):
        self.asset_manager = asset_manager or AssetManager()
        self.index_path = self.asset_manager.projects_dir / "index.json"

    def save(self, project: Project) -> Dict[str, object]:
        project_id = self._project_id(project)
        project_dir = self.asset_manager.get_project_dir(project_id)
        project_dir.mkdir(parents=True, exist_ok=True)
        project_path = project_dir / "project.json"
        payload = asdict(project)
        payload.setdefault("metadata", {})["project_id"] = project_id
        project_path.write_text(
            json.dumps(payload, indent=2),
            encoding="utf-8",
        )

        item = self._index_item(project_id, project, project_path)
        self._upsert_index(item)
        return item

    def list(self) -> List[Dict[str, object]]:
        return sorted(
            self._read_index(),
            key=lambda item: str(item.get("updated_at", "")),
            reverse=True,
        )

    def load_data(self, project_id: str) -> Dict[str, object]:
        project_path = self._project_path(project_id)
        if not project_path.exists():
            raise FileNotFoundError(f"Project {project_id} was not found.")

        return json.loads(project_path.read_text(encoding="utf-8"))

    def delete(self, project_id: str) -> None:
        safe_id = safe_project_id(project_id)
        project_dir = self.asset_manager.get_project_dir(safe_id)
        if project_dir.exists():
            rmtree(project_dir)

        self._write_index([
            item for item in self._read_index()
            if item.get("project_id") != safe_id
        ])

    def rename(self, project_id: str, title: str) -> Dict[str, object]:
        data = self.load_data(project_id)
        data["title"] = title
        metadata = data.setdefault("metadata", {})
        safe_id = safe_project_id(project_id)
        metadata["project_id"] = safe_id
        project_path = self._project_path(safe_id)
        project_path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

        item = self._index_item_from_data(safe_id, data, project_path)
        self._upsert_index(item)
        return item

    def duplicate(self, project_id: str, title: Optional[str] = None) -> Dict[str, object]:
        source_id = safe_project_id(project_id)
        source_dir = self.asset_manager.get_project_dir(source_id)
        if not source_dir.exists():
            raise FileNotFoundError(f"Project {source_id} was not found.")

        new_id = safe_project_id(f"{source_id}-{uuid4().hex[:8]}")
        destination_dir = self.asset_manager.get_project_dir(new_id)
        copytree(source_dir, destination_dir)

        project_path = destination_dir / "project.json"
        data = json.loads(project_path.read_text(encoding="utf-8"))
        data["title"] = title or f"{data.get('title', 'Untitled Project')} Copy"
        metadata = data.setdefault("metadata", {})
        metadata["project_id"] = new_id
        project_path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

        item = self._index_item_from_data(new_id, data, project_path)
        self._upsert_index(item)
        return item

    def _project_id(self, project: Project) -> str:
        return safe_project_id(
            project.metadata.get("project_id")
            or project.title
            or str(uuid4())
        )

    def _project_path(self, project_id: str) -> Path:
        return self.asset_manager.get_project_dir(safe_project_id(project_id)) / "project.json"

    def _index_item(
        self,
        project_id: str,
        project: Project,
        project_path: Path,
    ) -> Dict[str, object]:
        return {
            "project_id": project_id,
            "title": project.title,
            "project_type": project.project_type,
            "style": project.style,
            "scene_count": len(project.scenes),
            "path": str(project_path),
            "updated_at": self._now(),
        }

    def _index_item_from_data(
        self,
        project_id: str,
        data: Dict[str, object],
        project_path: Path,
    ) -> Dict[str, object]:
        return {
            "project_id": project_id,
            "title": data.get("title", "Untitled Project"),
            "project_type": data.get("project_type", "Custom"),
            "style": data.get("style", ""),
            "scene_count": len(data.get("scenes", [])),
            "path": str(project_path),
            "updated_at": self._now(),
        }

    def _read_index(self) -> List[Dict[str, object]]:
        if not self.index_path.exists():
            return []

        return json.loads(self.index_path.read_text(encoding="utf-8"))

    def _write_index(self, items: List[Dict[str, object]]) -> None:
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(
            json.dumps(items, indent=2),
            encoding="utf-8",
        )

    def _upsert_index(self, item: Dict[str, object]) -> None:
        items = [
            existing for existing in self._read_index()
            if existing.get("project_id") != item.get("project_id")
        ]
        items.append(item)
        self._write_index(items)

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()