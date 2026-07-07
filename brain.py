class DirectorBrain:

    def think(
        self,
        lyric: str,
        emotion: str,
        scene_type: str,
    ) -> dict:

        text = lyric.lower()

        decisions = {
            "location": "neutral cinematic space",
            "environment": "indoor",
            "time_of_day": "day",
            "weather": "clear",
            "lighting": "natural soft light",
            "mood": emotion,
            "dominant_color_palette": "natural tones",
            "action": "existing in the moment",
            "expression": emotion,
            "continuity_notes": "maintain visual continuity with the previous scene",
            "characters": [],
            "directorial_beats": {},
        }

        # Performance
        if scene_type == "performance":

            decisions["location"] = "cinematic performance stage"
            decisions["environment"] = "indoor"
            decisions["lighting"] = "dramatic concert lighting"
            decisions["time_of_day"] = "night"
            decisions["action"] = "performing directly to camera"
            decisions["expression"] = emotion

        # Action
        elif scene_type == "action":

            decisions["location"] = "urban street"
            decisions["environment"] = "outdoor"
            decisions["lighting"] = "hard contrast lighting"
            decisions["time_of_day"] = "night"
            decisions["action"] = "running forward"
            decisions["expression"] = emotion

        # Dream
        elif scene_type == "dream":

            decisions["location"] = "surreal dream landscape"
            decisions["environment"] = "outdoor"
            decisions["lighting"] = "soft glowing light"
            decisions["weather"] = "floating mist"
            decisions["time_of_day"] = "timeless"
            decisions["mood"] = "dreamlike"
            decisions["action"] = "floating peacefully"
            decisions["expression"] = emotion

        # Flashback
        elif scene_type == "flashback":

            decisions["location"] = "childhood neighborhood"
            decisions["environment"] = "outdoor"
            decisions["lighting"] = "warm sunset"
            decisions["time_of_day"] = "golden hour"
            decisions["mood"] = "nostalgic"
            decisions["action"] = "remembering the past"
            decisions["expression"] = emotion

        # Symbolic
        elif scene_type == "symbolic":

            decisions["location"] = "above the clouds"
            decisions["environment"] = "outdoor"
            decisions["lighting"] = "heavenly volumetric light"
            decisions["weather"] = "light fog"
            decisions["time_of_day"] = "sunrise"
            decisions["mood"] = "transcendent"
            decisions["action"] = "standing with confidence"
            decisions["expression"] = emotion

        self._apply_world_rules(text, decisions)
        self._add_directorial_beats(text, emotion, decisions)
        self._add_default_character(decisions, emotion)

        return decisions

    def _apply_world_rules(
        self,
        text: str,
        decisions: dict,
    ) -> None:

        if "fire" in text:
            decisions["lighting"] = "warm flickering light"
            decisions["dominant_color_palette"] = "orange and amber"
            decisions["mood"] = "intense"

        if "rain" in text:
            decisions["weather"] = "rain"
            decisions["lighting"] = "overcast soft light"
            decisions["mood"] = "melancholic"

        if "heaven" in text:
            decisions["location"] = "open sky threshold"
            decisions["environment"] = "outdoor"
            decisions["lighting"] = "bright soft light"
            decisions["dominant_color_palette"] = "white and gold"
            decisions["mood"] = "hopeful"

        if "city" in text:
            decisions["location"] = "urban city street"
            decisions["environment"] = "outdoor"

        if "forest" in text:
            decisions["location"] = "woodland forest"
            decisions["environment"] = "outdoor"
            decisions["dominant_color_palette"] = "deep green and earth tones"

        if "night" in text:
            decisions["time_of_day"] = "night"
            decisions["lighting"] = "low key night lighting"

        if "sunrise" in text:
            decisions["time_of_day"] = "golden hour"
            decisions["lighting"] = "warm sunrise light"
            decisions["dominant_color_palette"] = "gold and soft blue"

    def _add_directorial_beats(
        self,
        text: str,
        emotion: str,
        decisions: dict,
    ) -> None:
        beats = {
            "camera_intent": "observe the scene with restrained cinematic focus",
            "actor_direction": decisions["action"],
            "lighting_shift": "hold lighting steady",
            "atmosphere_change": "maintain atmosphere",
            "music_intensity": "medium",
            "cut_suggestion": "hold the shot",
        }

        if emotion in ["sad", "neutral"]:
            beats["camera_intent"] = "slowly dolly closer to the character"
            beats["music_intensity"] = "low"
            beats["cut_suggestion"] = "linger before cutting"

        if emotion in ["aggressive", "confident"]:
            beats["camera_intent"] = "push in with stronger visual pressure"
            beats["music_intensity"] = "high"
            beats["cut_suggestion"] = "cut on movement"

        if "rain" in text:
            beats["atmosphere_change"] = "rain begins or continues through the scene"
            beats["lighting_shift"] = "cool the lighting and soften contrast"

        if "fire" in text:
            beats["atmosphere_change"] = "heat shimmer and firelight intensify"
            beats["lighting_shift"] = "shift warmer with flickering highlights"

        if "stop" in text or "still" in text:
            beats["actor_direction"] = "stop moving and hold emotional tension"
            beats["cut_suggestion"] = "cut to close-up"

        decisions["directorial_beats"] = beats

    def _add_default_character(
        self,
        decisions: dict,
        emotion: str,
    ) -> None:

        decisions["characters"] = [
            {
                "id": "character_1",
                "name": "",
                "description": "default scene character",
                "facial_expression": decisions["expression"],
                "emotional_state": emotion,
                "current_location": decisions["location"],
            }
        ]
