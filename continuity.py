class ContinuityDirector:
    # ContinuityDirector only keeps scenes visually and narratively consistent.
    # It does not create scenes, choose cameras, generate prompts, or create shots.
    def maintain(
        self,
        previous_scene,
        current_scene,
        project,
    ):

        notes = []

        if previous_scene is None:
            current_scene.continuity = False
            current_scene.use_last_frame = False
            notes.append("first scene establishes the visual baseline")
            current_scene.continuity_notes = self._notes(current_scene, notes)
            return current_scene

        current_text = current_scene.lyrics.lower()

        if previous_scene.location == current_scene.location:
            current_scene.continuity = True
            current_scene.use_last_frame = True
            notes.append("same location continues across scenes")

        if (
            previous_scene.time_of_day == "night"
            and not self._time_changes(current_text)
        ):
            current_scene.time_of_day = previous_scene.time_of_day
            notes.append("night continuity preserved")

        if previous_scene.weather == current_scene.weather:
            notes.append("weather remains consistent")
        elif not self._weather_changes(current_text):
            current_scene.weather = previous_scene.weather
            notes.append("weather carried forward from previous scene")

        if previous_scene.mood == current_scene.mood:
            current_scene.dominant_color_palette = (
                previous_scene.dominant_color_palette
            )
            notes.append("matching mood preserves the color palette")

        if (
            self._same_character(project)
            and previous_scene.emotion == current_scene.emotion
        ):
            current_scene.expression = previous_scene.expression
            notes.append("same character and emotion preserve expression")

        current_scene.continuity_notes = self._notes(current_scene, notes)

        return current_scene

    def _time_changes(self, text: str) -> bool:
        time_words = [
            "day",
            "dawn",
            "morning",
            "noon",
            "sunrise",
            "sunset",
            "golden hour",
        ]

        return any(word in text for word in time_words)

    def _weather_changes(self, text: str) -> bool:
        weather_words = [
            "clear",
            "fog",
            "mist",
            "rain",
            "snow",
            "storm",
            "sunny",
            "wind",
        ]

        return any(word in text for word in weather_words)

    def _same_character(self, project) -> bool:
        return bool(
            project.metadata.get("character_image")
            or project.metadata.get("main_character")
        )

    def _notes(self, current_scene, notes):
        all_notes = []

        if current_scene.continuity_notes:
            all_notes.append(current_scene.continuity_notes)

        all_notes.extend(notes)

        return "; ".join(all_notes)


class ContinuityEngine:
    def generate_metadata(self, previous_scene, current_scene) -> dict:
        metadata = {
            "previous_location": self._previous_value(previous_scene, "location"),
            "location": current_scene.location,
            "lighting": current_scene.lighting,
            "weather": current_scene.weather,
            "time_of_day": current_scene.time_of_day,
            "camera_direction": self._camera_direction(current_scene),
            "character_positions": self._character_positions(current_scene),
            "character_clothing": self._character_clothing(current_scene),
            "props": self._props(current_scene),
            "dominant_colors": current_scene.dominant_color_palette,
        }

        current_scene.continuity_metadata = metadata

        return metadata

    def _previous_value(self, previous_scene, field_name: str) -> str:
        if previous_scene is None:
            return ""

        return getattr(previous_scene, field_name, "")

    def _camera_direction(self, scene) -> dict:
        return {
            "camera": scene.camera,
            "lens": scene.lens,
            "movement": scene.movement,
        }

    def _character_positions(self, scene) -> dict:
        return {
            character.id: character.current_location
            for character in scene.characters
        }

    def _character_clothing(self, scene) -> dict:
        return {
            character.id: character.clothing
            for character in scene.characters
        }

    def _props(self, scene) -> dict:
        return {
            character.id: character.props
            for character in scene.characters
        }
