from typing import List

from project import Project


class ContinuityManager:
    def review(self, project: Project) -> List[str]:
        issues = []
        previous_scene = None

        for scene in project.scenes:
            if not scene.continuity_notes:
                issues.append(
                    f"Scene {scene.scene_number:03d} has no continuity notes."
                )

            if previous_scene and scene.continuity:
                self._review_continuous_scene(previous_scene, scene, issues)

            previous_scene = scene

        print(f"Continuity Manager found {len(issues)} continuity notes to review.")

        return issues

    def _review_continuous_scene(
        self,
        previous_scene,
        scene,
        issues: List[str],
    ) -> None:
        if previous_scene.location != scene.location:
            issues.append(
                f"Scene {scene.scene_number:03d} is marked continuous "
                "but changes location."
            )

        if previous_scene.weather != scene.weather:
            issues.append(
                f"Scene {scene.scene_number:03d} is marked continuous "
                "but changes weather."
            )
