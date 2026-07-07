import json
from dataclasses import asdict
from pathlib import Path


class Exporter:
    @staticmethod
    def export(project, output_dir: str = "output") -> None:
        output_path = Path(output_dir)
        scenes_path = output_path / "scenes"
        prompts_path = output_path / "prompts"

        scenes_path.mkdir(parents=True, exist_ok=True)
        prompts_path.mkdir(parents=True, exist_ok=True)

        Exporter._write_json(output_path / "project.json", asdict(project))

        for scene in project.scenes:
            scene_name = f"scene_{scene.scene_number:03d}"
            Exporter._write_json(scenes_path / f"{scene_name}.json", asdict(scene))
            Exporter._write_text(prompts_path / f"{scene_name}_prompt.txt", scene.prompt)

    @staticmethod
    def _write_json(path: Path, data: dict) -> None:
        path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def _write_text(path: Path, text: str) -> None:
        path.write_text(
            text,
            encoding="utf-8",
        )
