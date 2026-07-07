from typing import Dict


class CameraLanguage:
    SUPPORTED_SHOTS = [
        "wide",
        "close-up",
        "medium",
        "extreme close-up",
        "tracking",
        "dolly",
        "crane",
        "orbit",
        "handheld",
        "drone",
        "steadicam",
        "POV",
        "over-the-shoulder",
    ]

    def normalize(
        self,
        camera: str,
        movement: str,
    ) -> Dict[str, str]:
        text = f"{camera} {movement}".lower()

        return {
            "shot": self._shot(text),
            "movement": self._movement(text),
            "style": self._style(text),
            "raw_camera": camera,
            "raw_movement": movement,
        }

    def _shot(self, text: str) -> str:
        if "extreme close" in text:
            return "extreme close-up"

        if "close" in text:
            return "close-up"

        if "wide" in text:
            return "wide"

        if "over shoulder" in text or "over-the-shoulder" in text:
            return "over-the-shoulder"

        if "pov" in text:
            return "POV"

        return "medium"

    def _movement(self, text: str) -> str:
        if "tracking" in text:
            return "tracking"

        if "dolly" in text or "push" in text:
            return "dolly"

        if "crane" in text:
            return "crane"

        if "orbit" in text:
            return "orbit"

        if "drone" in text:
            return "drone"

        if "steadicam" in text or "steadycam" in text:
            return "steadicam"

        if "handheld" in text:
            return "handheld"

        return "locked"

    def _style(self, text: str) -> str:
        if "handheld" in text:
            return "handheld"

        if "steadicam" in text or "steadycam" in text:
            return "steadicam"

        if "drone" in text:
            return "drone"

        return "cinematic"
