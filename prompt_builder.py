from typing import Dict, List

from scene import Scene


class PromptBuilder:

    def build(self, scene: Scene) -> str:
        scene.prompt_layers = self.build_layers(scene)
        return self.assemble(scene.prompt_layers)

    def build_layers(self, scene: Scene) -> Dict[str, str]:
        return {
            "character": self._character_layer(scene),
            "environment": self._environment_layer(scene),
            "direction": self._direction_layer(scene),
            "lighting": self._lighting_layer(scene),
            "camera": self._camera_layer(scene),
            "emotion": self._emotion_layer(scene),
            "continuity": self._continuity_layer(scene),
            "style": self._style_layer(scene),
            "motion": self._motion_layer(scene),
            "fx": self._fx_layer(scene),
            "negative_prompt": self._negative_prompt_layer(),
        }

    def assemble(self, layers: Dict[str, str]) -> str:
        ordered_layers = [
            "character",
            "environment",
            "direction",
            "camera",
            "lighting",
            "emotion",
            "style",
            "continuity",
            "motion",
            "fx",
            "negative_prompt",
        ]

        return "\n\n".join(
            layers[layer]
            for layer in ordered_layers
            if layers.get(layer)
        ).strip()

    def _character_layer(self, scene: Scene) -> str:
        character_lines = self._character_lines(scene)

        return "\n".join([
            "Character:",
            *character_lines,
            f"Character Action: {scene.action}",
            f"Facial Expression: {scene.expression}",
        ])

    def _environment_layer(self, scene: Scene) -> str:
        return "\n".join([
            "Environment:",
            f"Scene Type: {scene.scene_type}",
            f"Source Text: {scene.lyrics}",
            f"Location: {scene.location}",
            f"Environment Type: {scene.environment}",
            f"Weather: {scene.weather}",
            f"Time of Day: {scene.time_of_day}",
        ])

    def _direction_layer(self, scene: Scene) -> str:
        beats = scene.directorial_beats

        return "\n".join([
            "Direction:",
            f"Camera Intent: {beats.get('camera_intent', '')}",
            f"Actor Direction: {beats.get('actor_direction', scene.action)}",
            f"Lighting Shift: {beats.get('lighting_shift', '')}",
            f"Atmosphere Change: {beats.get('atmosphere_change', '')}",
            f"Music Intensity: {beats.get('music_intensity', '')}",
            f"Cut Suggestion: {beats.get('cut_suggestion', '')}",
        ])

    def _lighting_layer(self, scene: Scene) -> str:
        return "\n".join([
            "Lighting:",
            scene.lighting,
            f"Dominant Color Palette: {scene.dominant_color_palette}",
        ])

    def _camera_layer(self, scene: Scene) -> str:
        return "\n".join([
            "Camera:",
            f"Shot: {scene.camera_language.get('shot', scene.camera)}",
            f"Movement: {scene.camera_language.get('movement', scene.movement)}",
            f"Style: {scene.camera_language.get('style', 'cinematic')}",
            f"Lens: {scene.lens}",
        ])

    def _emotion_layer(self, scene: Scene) -> str:
        return "\n".join([
            "Emotion:",
            f"Scene Emotion: {scene.emotion}",
            f"Mood: {scene.mood}",
        ])

    def _continuity_layer(self, scene: Scene) -> str:
        return "\n".join([
            "Continuity:",
            scene.continuity_notes,
            f"Metadata: {scene.continuity_metadata}",
        ])

    def _style_layer(self, scene: Scene) -> str:
        return "\n".join([
            "Style:",
            "Ultra cinematic.",
            "Photorealistic.",
            "Hollywood feature film.",
            "Natural skin.",
            "Realistic clothing physics.",
            "Volumetric lighting.",
            "8K.",
            "Extremely detailed.",
        ])

    def _motion_layer(self, scene: Scene) -> str:
        return "\n".join([
            "Motion:",
            scene.movement,
        ])

    def _fx_layer(self, scene: Scene) -> str:
        return "\n".join([
            "FX:",
            "natural atmospheric detail",
        ])

    def _negative_prompt_layer(self) -> str:
        return "\n".join([
            "Negative Prompt:",
            "low quality, distorted faces, broken anatomy, flicker",
        ])

    def _character_lines(self, scene: Scene) -> List[str]:
        if not scene.characters:
            return ["No named character specified."]

        return [
            f"{character.id}: {character.description}"
            for character in scene.characters
        ]
