from typing import List

from scene import Scene
from emotion import EmotionEngine
from camera import CameraDirector


class GhostDirector:

    def __init__(self):
        print("🎬 Ghost Director Initialized")

        self.emotion_engine = EmotionEngine()
        self.camera_director = CameraDirector()

    def analyze(
        self,
        song_path: str,
        lyrics: str,
        character_image: str,
        style: str,
        scene_length: int = 15,
    ) -> List[Scene]:

        print("🎬 Analyzing project...")
        print(f"Song: {song_path}")
        print(f"Character: {character_image}")
        print(f"Style: {style}")
        print()

        scenes = []

        lyric_lines = [
            line.strip()
            for line in lyrics.split("\n")
            if line.strip()
        ]

        current_time = 0.0

        for i, line in enumerate(lyric_lines):

            emotion = self.emotion_engine.detect(line)

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
                scene_type="performance",
                emotion=emotion,
                energy="medium",

                # Visuals
                location="",
                lighting="",
                weather="",
                time_of_day="",

                # Camera
                camera=shot["camera"],
                lens=shot["lens"],
                movement=shot["movement"],

                # Character
                action="",
                expression="",

                # Continuity
                continuity=i > 0,
                use_last_frame=i > 0,

                # Prompt
                prompt=""
            )

            scenes.append(scene)

            current_time += scene_length

        print(f"✅ Created {len(scenes)} scenes")

        return scenes


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