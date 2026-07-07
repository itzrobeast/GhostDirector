from typing import List, Optional

from asset_manager import AssetManager
from project import Project


class Editor:
    def __init__(self, asset_manager: Optional[AssetManager] = None):
        self.asset_manager = asset_manager or AssetManager()

    def prepare(self, project: Project) -> List[str]:
        rendered_videos = []

        for scene in project.scenes:
            if scene.rendered_video:
                rendered_videos.append(scene.rendered_video)
                continue

            managed_video = self.asset_manager.get_scene_video(scene.scene_number)
            if managed_video.exists():
                rendered_videos.append(str(managed_video))

        print(f"Editor collected {len(rendered_videos)} rendered scene videos.")

        return rendered_videos
