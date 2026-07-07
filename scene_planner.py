from typing import List

from project import Project
from scene import Scene


class ScenePlanner:
    # ScenePlanner decides where scene boundaries are.
    # It intentionally avoids emotion, camera, prompt, and creative decisions.
    def plan(
        self,
        project: Project,
        story: str,
        scene_length: int = 15,
    ) -> List[Scene]:

        scene_texts = self._split_story(project, story)
        scenes = []
        current_time = 0.0

        for i, text in enumerate(scene_texts):
            scene = Scene(

                # Scene
                scene_number=i + 1,

                # Timing
                start_time=current_time,
                duration=scene_length,

                # Source
                lyrics=text,

                # Story
                scene_type="unclassified",
                emotion="",
                energy="medium",

                # Visuals
                location="",
                lighting="",
                weather="",
                time_of_day="",

                # Camera
                camera="",
                lens="",
                movement="",

                # Character
                action="",
                expression="",

                # Continuity
                continuity=i > 0,
                use_last_frame=i > 0,

                # Prompt
                prompt="",
            )

            scenes.append(scene)
            current_time += scene_length

        return scenes

    def _split_story(
        self,
        project: Project,
        story: str,
    ) -> List[str]:

        if project.project_type in ["lyrics", "music_video"]:
            return [
                line.strip()
                for line in story.split("\n")
                if line.strip()
            ]

        paragraphs = [
            paragraph.strip()
            for paragraph in story.split("\n\n")
            if paragraph.strip()
        ]

        if paragraphs:
            return paragraphs

        return [
            line.strip()
            for line in story.split("\n")
            if line.strip()
        ]
