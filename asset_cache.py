from typing import Dict

from project import Project


class AssetCache:
    def register_project_assets(self, project: Project) -> Dict[str, str]:
        assets = {}

        for scene in project.scenes:
            if scene.rendered_video:
                asset_id = f"scene_{scene.scene_number:03d}_video"
                assets[asset_id] = scene.rendered_video

        print(f"Asset Cache registered {len(assets)} rendered assets.")

        return assets
