import random


class CameraDirector:

    def choose(self, emotion: str) -> dict:

        shots = {

            "confident": [
                {
                    "camera": "low angle",
                    "lens": "35mm",
                    "movement": "slow dolly in",
                },
                {
                    "camera": "hero shot",
                    "lens": "50mm",
                    "movement": "orbit",
                },
            ],

            "aggressive": [
                {
                    "camera": "handheld",
                    "lens": "24mm",
                    "movement": "fast tracking",
                },
                {
                    "camera": "low angle",
                    "lens": "28mm",
                    "movement": "push in",
                },
            ],

            "happy": [
                {
                    "camera": "wide shot",
                    "lens": "35mm",
                    "movement": "crane",
                },
                {
                    "camera": "medium shot",
                    "lens": "50mm",
                    "movement": "steadycam",
                },
            ],

            "sad": [
                {
                    "camera": "close up",
                    "lens": "85mm",
                    "movement": "slow push",
                },
                {
                    "camera": "over shoulder",
                    "lens": "85mm",
                    "movement": "locked",
                },
            ],

            "neutral": [
                {
                    "camera": "medium shot",
                    "lens": "50mm",
                    "movement": "slow dolly",
                }
            ],
        }

        return random.choice(shots.get(emotion, shots["neutral"]))