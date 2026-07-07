from dataclasses import dataclass, field
from typing import List, Optional

from asset_cache import AssetCache
from asset_manager import AssetManager
from brain import DirectorBrain
from camera import CameraDirector
from camera_language import CameraLanguage
from character import Character
from continuity import ContinuityDirector, ContinuityEngine
from continuity_manager import ContinuityManager
from editor import Editor
from emotion import EmotionEngine
from exporter import Exporter
from project import Project
from prompt_builder import PromptBuilder
from renderer import Renderer
from scene import Scene
from scene_planner import ScenePlanner
from timeline import Timeline


@dataclass
class PipelineRunConfig:
    export: bool = True
    render: bool = True
    edit: bool = True
    continuity_review: bool = True
    cache_assets: bool = True
    render_scene_numbers: List[int] = field(default_factory=list)


class Pipeline:
    def __init__(self):
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

    def run(
        self,
        project: Project,
        scene_length: int = 15,
        config: Optional[PipelineRunConfig] = None,
    ) -> List[Scene]:
        run_config = config or PipelineRunConfig()
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
            self._direct_scene(
                project,
                scene,
                previous_scene,
                default_scene_type,
            )
            previous_scene = scene

        project.scenes = scenes
        project.timeline = Timeline.from_scenes(scenes)
        self._run_output_stages(project, run_config)

        return scenes

    def _run_output_stages(
        self,
        project: Project,
        config: PipelineRunConfig,
    ) -> None:
        if config.export:
            Exporter.export(project, self.asset_manager)

        if config.render:
            self.renderer.render(
                project,
                scene_numbers=config.render_scene_numbers,
            )

        if config.edit:
            self.editor.prepare(project)

        if config.continuity_review:
            self.continuity_manager.review(project)

        if config.cache_assets:
            self.asset_cache.register_project_assets(project)

        if config.export and (config.render or config.cache_assets):
            Exporter.export(project, self.asset_manager)

    def _direct_scene(
        self,
        project: Project,
        scene: Scene,
        previous_scene,
        default_scene_type: str,
    ) -> None:
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
        scene.directorial_beats = creative_direction["directorial_beats"]
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
