from typing import List

from project import Project


class Editor:
    def prepare(self, project: Project) -> List[str]:
        rendered_videos = [
            scene.rendered_video
            for scene in project.scenes
            if scene.rendered_video
        ]

        print(f"Editor collected {len(rendered_videos)} rendered scene videos.")

        return rendered_videos
