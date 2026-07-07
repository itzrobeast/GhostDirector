from typing import List

from scene import Scene
from asset_cache import AssetCache
from asset_manager import AssetManager
from emotion import EmotionEngine
from camera import CameraDirector
from camera_language import CameraLanguage
from brain import DirectorBrain
from character import Character
from continuity import ContinuityDirector, ContinuityEngine
from continuity_manager import ContinuityManager
from editor import Editor
from exporter import Exporter
from prompt_builder import PromptBuilder
from project import Project
from renderer import Renderer
from scene_planner import ScenePlanner
from timeline import Timeline


class GhostDirector:

    def __init__(self):
        print("Ghost Director Initialized")

        self.asset_manager = AssetManager()
        self.asset_cache = AssetCache()
        self.emotion_engine = EmotionEngine()
        self.camera_director = CameraDirector()
        self.camera_language = CameraLanguage()
        self.director_brain = DirectorBrain()
        self.continuity_director = ContinuityDirector()
        self.continuity_engine = ContinuityEngine()
        self.continuity_manager = ContinuityManager()
        self.editor = Editor(self.asset_manager)
        self.prompt_builder = PromptBuilder()
        self.renderer = Renderer(self.asset_manager)
        self.scene_planner = ScenePlanner()

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

        story = project.source_text
        scenes = self.scene_planner.plan(
            project,
            story,
            scene_length=scene_length,
        )
        default_scene_type = project.metadata.get(
            "default_scene_type",
            "unclassified",
        )
        previous_scene = None

        for scene in scenes:

            emotion = self.emotion_engine.detect(scene.lyrics)
            scene_type = default_scene_type
            creative_direction = self.director_brain.think(
                lyric=scene.lyrics,
                emotion=emotion,
                scene_type=scene_type,
            )

            scene.scene_type = scene_type
            scene.emotion = emotion
            scene.location = creative_direction["location"]
            scene.environment = creative_direction["environment"]
            scene.lighting = creative_direction["lighting"]
            scene.weather = creative_direction["weather"]
            scene.time_of_day = creative_direction["time_of_day"]
            scene.mood = creative_direction["mood"]
            scene.dominant_color_palette = creative_direction[
                "dominant_color_palette"
            ]
            scene.action = creative_direction["action"]
            scene.expression = creative_direction["expression"]
            scene.continuity_notes = creative_direction["continuity_notes"]
            scene.characters = self._build_characters(
                creative_direction["characters"]
            )
            scene.character_ids = self._register_characters(
                project,
                scene.characters,
            )

            self.continuity_director.maintain(
                previous_scene,
                scene,
                project,
            )

            shot = self.camera_director.choose(emotion)

            scene.camera = shot["camera"]
            scene.lens = shot["lens"]
            scene.movement = shot["movement"]
            scene.camera_language = self.camera_language.normalize(
                scene.camera,
                scene.movement,
            )
            self.continuity_engine.generate_metadata(previous_scene, scene)
            scene.prompt = self.prompt_builder.build(scene)
            previous_scene = scene

        project.scenes = scenes
        project.timeline = Timeline.from_scenes(scenes)
        Exporter.export(project, self.asset_manager)
        self.renderer.render(project)
        self.editor.prepare(project)
        self.continuity_manager.review(project)
        self.asset_cache.register_project_assets(project)

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
                "default_scene_type": "performance",
            },
        )

        return self.direct_project(
            project=project,
            scene_length=scene_length,
        )

    def _build_characters(self, character_data) -> List[Character]:
        return [
            Character(**character)
            for character in character_data
        ]

    def _register_characters(
        self,
        project: Project,
        characters: List[Character],
    ) -> List[str]:
        character_ids = []

        for character in characters:
            registered = project.character_registry.register(character)
            character_ids.append(registered.id)

        return character_ids


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
