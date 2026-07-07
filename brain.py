class DirectorBrain:

    def think(
        self,
        lyric: str,
        emotion: str,
        scene_type: str,
    ) -> dict:

        decisions = {
            "location": "",
            "lighting": "",
            "weather": "",
            "time_of_day": "",
            "action": "",
            "expression": "",
        }

        # Performance
        if scene_type == "performance":

            decisions["location"] = "cinematic performance stage"
            decisions["lighting"] = "dramatic concert lighting"
            decisions["time_of_day"] = "night"
            decisions["action"] = "performing directly to camera"
            decisions["expression"] = emotion

        # Action
        elif scene_type == "action":

            decisions["location"] = "urban street"
            decisions["lighting"] = "hard contrast lighting"
            decisions["time_of_day"] = "night"
            decisions["action"] = "running forward"
            decisions["expression"] = emotion

        # Dream
        elif scene_type == "dream":

            decisions["location"] = "surreal dream landscape"
            decisions["lighting"] = "soft glowing light"
            decisions["weather"] = "floating mist"
            decisions["time_of_day"] = "timeless"
            decisions["action"] = "floating peacefully"
            decisions["expression"] = emotion

        # Flashback
        elif scene_type == "flashback":

            decisions["location"] = "childhood neighborhood"
            decisions["lighting"] = "warm sunset"
            decisions["time_of_day"] = "golden hour"
            decisions["action"] = "remembering the past"
            decisions["expression"] = emotion

        # Symbolic
        elif scene_type == "symbolic":

            decisions["location"] = "above the clouds"
            decisions["lighting"] = "heavenly volumetric light"
            decisions["weather"] = "light fog"
            decisions["time_of_day"] = "sunrise"
            decisions["action"] = "standing with confidence"
            decisions["expression"] = emotion

        return decisions