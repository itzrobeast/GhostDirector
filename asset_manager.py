from pathlib import Path
from shutil import copy2
from typing import Optional

from config import DEFAULT_CONFIG


class AssetManager:
    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = Path(output_dir or DEFAULT_CONFIG.output_dir)
        self.projects_dir = self.output_dir / "projects"
        self.scenes_dir = self.output_dir / "scenes"
        self.prompts_dir = self.output_dir / "prompts"
        self.videos_dir = self.output_dir / "videos"
        self.audio_dir = self.output_dir / "audio"
        self.cache_dir = self.output_dir / "cache"
        self.ensure_directories()

    def ensure_directories(self) -> None:
        for path in [
            self.output_dir,
            self.projects_dir,
            self.scenes_dir,
            self.prompts_dir,
            self.videos_dir,
            self.audio_dir,
            self.cache_dir,
        ]:
            path.mkdir(parents=True, exist_ok=True)

    def get_project_json(self) -> Path:
        return self.projects_dir / "project.json"

    def get_production_status_json(self) -> Path:
        return self.projects_dir / "production_status.json"

    def get_render_queue_json(self) -> Path:
        return self.projects_dir / "render_queue.json"

    def get_edit_decision_list_json(self) -> Path:
        return self.projects_dir / "edit_decision_list.json"

    def get_timeline_json(self) -> Path:
        return self.projects_dir / "timeline.json"

    def get_final_movie(self) -> Path:
        return self.videos_dir / "final_movie.mp4"

    def get_scene_video(self, scene_number: int) -> Path:
        return self.videos_dir / f"scene_{scene_number:03d}.mp4"

    def get_scene_prompt(self, scene_number: int) -> Path:
        return self.prompts_dir / f"scene_{scene_number:03d}_prompt.txt"

    def get_scene_json(self, scene_number: int) -> Path:
        return self.scenes_dir / f"scene_{scene_number:03d}.json"

    def normalize_scene_video(
        self,
        scene_number: int,
        source_video: str,
    ) -> str:
        managed_video = self.get_scene_video(scene_number)
        if not source_video:
            return str(managed_video)

        source_path = Path(source_video)
        if not source_path.exists():
            return str(managed_video)

        if source_path.resolve() == managed_video.resolve():
            return str(managed_video)

        managed_video.parent.mkdir(parents=True, exist_ok=True)
        copy2(source_path, managed_video)

        return str(managed_video)

    def normalize_final_movie(self, source_video: str) -> str:
        final_movie = self.get_final_movie()
        source_path = Path(source_video)

        if not source_video or not source_path.exists():
            return ""

        if source_path.resolve() == final_movie.resolve():
            return str(final_movie)

        final_movie.parent.mkdir(parents=True, exist_ok=True)
        copy2(source_path, final_movie)

        return str(final_movie)
