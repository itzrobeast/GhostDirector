import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from shutil import copyfileobj
from typing import BinaryIO, Dict, List, Optional
from uuid import uuid4

from asset_manager import AssetManager


@dataclass
class UploadedAsset:
    project_id: str
    id: str
    original_name: str
    stored_name: str
    category: str
    content_type: str
    size: int
    path: str
    thumbnail_path: Optional[str] = None


class AssetUploader:
    allowed_extensions = {
        ".mp3",
        ".wav",
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".mp4",
        ".mov",
        ".pdf",
        ".docx",
        ".txt",
        ".md",
        ".markdown",
        ".json",
    }
    audio_extensions = {".mp3", ".wav"}
    image_extensions = {".png", ".jpg", ".jpeg", ".webp"}
    video_extensions = {".mp4", ".mov"}
    document_extensions = {".pdf", ".docx", ".txt", ".md", ".markdown", ".json"}

    def __init__(self, asset_manager: Optional[AssetManager] = None):
        self.asset_manager = asset_manager or AssetManager()

    def save(
        self,
        project_id: str,
        filename: str,
        content_type: str,
        file: BinaryIO,
    ) -> UploadedAsset:
        extension = Path(filename).suffix.lower()
        if extension not in self.allowed_extensions:
            raise ValueError(f"Unsupported upload type: {extension or 'unknown'}")

        category = self._category_for_extension(extension)
        asset_id = str(uuid4())
        stored_name = f"{asset_id}{extension}"
        destination_dir = self.asset_manager.get_project_asset_category_dir(
            project_id,
            category,
        )
        destination_dir.mkdir(parents=True, exist_ok=True)
        destination = destination_dir / stored_name

        with destination.open("wb") as output_file:
            copyfileobj(file, output_file)

        asset = UploadedAsset(
            project_id=project_id,
            id=asset_id,
            original_name=filename,
            stored_name=stored_name,
            category=category,
            content_type=content_type,
            size=destination.stat().st_size,
            path=str(destination),
            thumbnail_path=self._thumbnail_for(project_id, destination, category),
        )
        self._append_manifest(project_id, asset)

        return asset

    def load_manifest(self, project_id: str) -> List[Dict[str, object]]:
        manifest_path = self.asset_manager.get_project_asset_manifest(project_id)
        if not manifest_path.exists():
            return []

        return json.loads(manifest_path.read_text(encoding="utf-8"))

    def _category_for_extension(self, extension: str) -> str:
        if extension in self.audio_extensions:
            return "audio"

        if extension in self.image_extensions:
            return "images"

        if extension in self.video_extensions:
            return "videos"

        if extension in self.document_extensions:
            return "documents"

        return "references"

    def _thumbnail_for(
        self,
        project_id: str,
        path: Path,
        category: str,
    ) -> Optional[str]:
        if category != "images":
            return None

        thumbnails_dir = self.asset_manager.get_project_asset_thumbnails_dir(
            project_id,
        )
        thumbnails_dir.mkdir(parents=True, exist_ok=True)
        thumbnail_path = thumbnails_dir / f"{path.stem}_thumb{path.suffix}"

        try:
            from PIL import Image
        except ImportError:
            return None

        with Image.open(path) as image:
            image.thumbnail((320, 320))
            image.save(thumbnail_path)

        return str(thumbnail_path)

    def _append_manifest(self, project_id: str, asset: UploadedAsset) -> None:
        manifest_path = self.asset_manager.get_project_asset_manifest(project_id)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest = self.load_manifest(project_id)
        manifest.append(asdict(asset))
        manifest_path.write_text(
            json.dumps(manifest, indent=2),
            encoding="utf-8",
        )


def safe_project_id(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]", "-", value).strip("-")
    return cleaned or str(uuid4())