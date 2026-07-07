class EmotionEngine:

    def detect(self, text: str) -> str:

        text = text.lower()

        confident = [
            "king",
            "boss",
            "power",
            "winner",
            "top",
            "strong",
            "fearless",
            "victory",
            "champion",
        ]

        aggressive = [
            "fight",
            "kill",
            "fire",
            "war",
            "rage",
            "blood",
            "burn",
            "enemy",
        ]

        happy = [
            "smile",
            "joy",
            "love",
            "dance",
            "laugh",
            "party",
            "shine",
        ]

        sad = [
            "alone",
            "cry",
            "pain",
            "lost",
            "broken",
            "dark",
            "tears",
        ]

        for word in confident:
            if word in text:
                return "confident"

        for word in aggressive:
            if word in text:
                return "aggressive"

        for word in happy:
            if word in text:
                return "happy"

        for word in sad:
            if word in text:
                return "sad"

        return "neutral"