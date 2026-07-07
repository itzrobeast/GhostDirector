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
