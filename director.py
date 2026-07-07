from typing import List

from scene import Scene
from emotion import EmotionEngine
from camera import CameraDirector
from brain import DirectorBrain
from prompt_builder import PromptBuilder
from project import Project


class GhostDirector:

    def __init__(self):
        print("Ghost Director Initialized")

        self.emotion_engine = EmotionEngine()
        self.camera_director = CameraDirector()
        self.director_brain = DirectorBrain()
        self.prompt_builder = PromptBuilder()

    def direct_project(
        self,
        project: Project,
        scene_length: int = 15,
    ) -> List[Scene]:

        print("Analyzing project...")
        print(f"Title: {project.title}")
        print(f"Type: {project.project_type}")
        print(f"Style: {project.style}")
        print()

        scenes = []

        source_lines = [
            line.strip()
            for line in project.source_text.split("\n")
            if line.strip()
        ]

        current_time = 0.0

        for i, line in enumerate(source_lines):

            emotion = self.emotion_engine.detect(line)
            scene_type = "performance"
            creative_direction = self.director_brain.think(
                lyric=line,
                emotion=emotion,
                scene_type=scene_type,
            )

            shot = self.camera_director.choose(emotion)

            scene = Scene(

                # Scene
                scene_number=i + 1,

                # Timing
                start_time=current_time,
                duration=scene_length,

                # Source
                lyrics=line,

                # Story
                scene_type=scene_type,
                emotion=emotion,
                energy="medium",

                # Visuals
                location=creative_direction["location"],
                lighting=creative_direction["lighting"],
                weather=creative_direction["weather"],
                time_of_day=creative_direction["time_of_day"],

                # Camera
                camera=shot["camera"],
                lens=shot["lens"],
                movement=shot["movement"],

                # Character
                action=creative_direction["action"],
                expression=creative_direction["expression"],

                # Continuity
                continuity=i > 0,
                use_last_frame=i > 0,

                # Prompt
                prompt="",
            )

            scene.prompt = self.prompt_builder.build(scene)
            scenes.append(scene)

            current_time += scene_length

        print(f"Created {len(scenes)} scenes")

        return scenes

    def analyze(
        self,
        song_path: str,
        lyrics: str,
        character_image: str,
        style: str,
        scene_length: int = 15,
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
            },
        )

        return self.direct_project(
            project=project,
            scene_length=scene_length,
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
