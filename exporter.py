import json
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from asset_manager import AssetManager
from production_status import ProductionStatus
from render_queue import RenderQueue


class Exporter:
    @staticmethod
    def export(
        project,
        asset_manager: Optional[AssetManager] = None,
    ) -> None:
        assets = asset_manager or AssetManager()

        Exporter._write_json(assets.get_project_json(), asdict(project))
        Exporter._write_json(
            assets.get_production_status_json(),
            asdict(ProductionStatus().review(project)),
        )
        Exporter._write_json(
            assets.get_render_queue_json(),
            [asdict(item) for item in RenderQueue().build(project)],
        )

        for scene in project.scenes:
            Exporter._write_json(
                assets.get_scene_json(scene.scene_number),
                asdict(scene),
            )
            Exporter._write_text(
                assets.get_scene_prompt(scene.scene_number),
                scene.prompt,
            )

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
