import json
from dataclasses import asdict
from typing import List, Optional

from asset_manager import AssetManager
from edit_decision import EditDecision
from project import Project


class Editor:
    def __init__(self, asset_manager: Optional[AssetManager] = None):
        self.asset_manager = asset_manager or AssetManager()

    def prepare(self, project: Project) -> List[str]:
        rendered_videos = []
        edit_decisions = []

        for scene in self._timeline_sorted_scenes(project):
            video_path = self._video_path(scene)
            if not video_path:
                continue

            rendered_videos.append(video_path)
            edit_decisions.append(self._edit_decision(project, scene, video_path))

        project.edit_decisions = edit_decisions
        project.rendered_video = self._assemble_final_movie(rendered_videos)
        self._export_edit_metadata(project)

        print(f"Editor collected {len(rendered_videos)} rendered scene videos.")

        return rendered_videos

    def _timeline_sorted_scenes(self, project: Project):
        timeline_order = {
            entry.scene_number: entry.start_time
            for entry in project.timeline.entries
        }

        return sorted(
            project.scenes,
            key=lambda scene: timeline_order.get(
                scene.scene_number,
                scene.start_time,
            ),
        )

    def _video_path(self, scene) -> str:
        if scene.rendered_video:
            return scene.rendered_video

        managed_video = self.asset_manager.get_scene_video(scene.scene_number)
        if managed_video.exists():
            return str(managed_video)

        return ""

    def _edit_decision(
        self,
        project: Project,
        scene,
        video_path: str,
    ) -> EditDecision:
        timeline_entry = self._timeline_entry(project, scene.scene_number)
        start_time = timeline_entry.start_time if timeline_entry else scene.start_time
        duration = timeline_entry.duration if timeline_entry else scene.duration
        transition = timeline_entry.transition if timeline_entry else "cut"

        return EditDecision(
            scene_number=scene.scene_number,
            video_path=video_path,
            start_time=start_time,
            end_time=start_time + duration,
            duration=duration,
            transition=transition,
        )

    def _timeline_entry(self, project: Project, scene_number: int):
        for entry in project.timeline.entries:
            if entry.scene_number == scene_number:
                return entry

        return None

    def _assemble_final_movie(self, rendered_videos: List[str]) -> str:
        if len(rendered_videos) != 1:
            return ""

        return self.asset_manager.normalize_final_movie(rendered_videos[0])

    def _export_edit_metadata(self, project: Project) -> None:
        self._write_json(
            self.asset_manager.get_edit_decision_list_json(),
            [asdict(decision) for decision in project.edit_decisions],
        )
        self._write_json(
            self.asset_manager.get_timeline_json(),
            asdict(project.timeline),
        )

    def _write_json(self, path, data) -> None:
        path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )
