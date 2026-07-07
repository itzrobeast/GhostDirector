from typing import List

from pipeline import Pipeline, PipelineRunConfig
from project import Project
from project_loader import ProjectLoader
from scene import Scene


class GhostDirector:

    def __init__(self):
        print("Ghost Director Initialized")
        self.pipeline = Pipeline()

    def direct_project(
        self,
        project: Project,
        scene_length: int = 15,
        run_config: PipelineRunConfig | None = None,
    ) -> List[Scene]:

        print("Analyzing project...")
        print(f"Title: {project.title}")
        print(f"Type: {project.project_type}")
        print(f"Style: {project.style}")
        print()

        scenes = self.pipeline.run(
            project,
            scene_length=scene_length,
            config=run_config,
        )

        print(f"Created {len(scenes)} scenes")

        return scenes

    def rerender_scenes(
        self,
        project: Project,
        scene_numbers: List[int],
    ) -> List[str]:
        return self.pipeline.rerender_scenes(
            project,
            scene_numbers,
        )

    def load_project(self, path: str = "output/projects/project.json") -> Project:
        return ProjectLoader.load(path)

    def rerender_project(
        self,
        scene_numbers: List[int] | None = None,
        path: str = "output/projects/project.json",
    ) -> List[str]:
        project = self.load_project(path)
        selected_scene_numbers = scene_numbers or [
            scene.scene_number for scene in project.scenes
        ]

        return self.rerender_scenes(project, selected_scene_numbers)

    def analyze(
        self,
        song_path: str,
        lyrics: str,
        character_image: str,
        style: str,
        scene_length: int = 15,
        run_config: PipelineRunConfig | None = None,
    ) -> List[Scene]:

        project = Project(
            title=song_path,
            project_type="music_video",
            source_text=lyrics,
            style=style,
            inputs=[song_path, character_image],
            metadata={
                "song_path": song_path,
                "character_image": character_image,
                "default_scene_type": "performance",
            },
        )

        return self.direct_project(
            project=project,
            scene_length=scene_length,
            run_config=run_config,
        )


if __name__ == "__main__":

    director = GhostDirector()

    song_path = input("Song file: ")
    lyrics_path = input("Lyrics file: ")
    character_image = input("Character image: ")
    style = input("Style: ")

    with open(lyrics_path, "r", encoding="utf-8") as f:
        lyrics = f.read()

    scenes = director.analyze(
        song_path=song_path,
        lyrics=lyrics,
        character_image=character_image,
        style=style,
        scene_length=15,
    )

    print()

    for scene in scenes:
        print("=" * 70)
        print(scene)
