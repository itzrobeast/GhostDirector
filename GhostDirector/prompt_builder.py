from scene import Scene


class PromptBuilder:

    def build(self, scene: Scene) -> str:

        prompt = f"""
Ultra cinematic.

Scene Type:
{scene.scene_type}

Lyrics:
{scene.lyrics}

Emotion:
{scene.emotion}

Location:
{scene.location}

Lighting:
{scene.lighting}

Weather:
{scene.weather}

Time of Day:
{scene.time_of_day}

Camera:
{scene.camera}

Lens:
{scene.lens}

Movement:
{scene.movement}

Character Action:
{scene.action}

Facial Expression:
{scene.expression}

Photorealistic.
Hollywood feature film.
Natural skin.
Realistic clothing physics.
Volumetric lighting.
8K.
Extremely detailed.
"""

        return prompt.strip()