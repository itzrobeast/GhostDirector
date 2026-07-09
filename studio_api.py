from dataclasses import asdict
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from asset_manager import AssetManager
from asset_upload import AssetUploader, safe_project_id
from director import GhostDirector
from pipeline import PipelineRunConfig
from project import Project

app = FastAPI(title="Ghost Director Studio API")
director = GhostDirector()
asset_uploader = AssetUploader()


def _path_available(path: Path) -> bool:
    if path.is_dir():
        return any(path.iterdir())

    return path.exists()


def _export_manifest(project: Project) -> list[dict]:
    assets = AssetManager()
    export_targets = [
        ("Project JSON", assets.get_project_json()),
        ("Production Status", assets.get_production_status_json()),
        ("Render Queue", assets.get_render_queue_json()),
        ("Scene JSON", assets.scenes_dir),
        ("Prompts", assets.prompts_dir),
        ("Timeline", assets.get_timeline_json()),
        ("Edit Decision List", assets.get_edit_decision_list_json()),
        ("Final Movie", assets.get_final_movie()),
        ("Assets", assets.output_dir),
    ]

    return [
        {
            "label": label,
            "path": str(path),
            "available": _path_available(path),
        }
        for label, path in export_targets
    ]


class ProjectInput(BaseModel):
    title: str = Field(..., min_length=1)
    project_id: Optional[str] = None
    project_type: str
    source_text: str
    style: str
    camera_style: str = "Hollywood"
    renderer: str = "Seedance"
    resolution: str = "1920x1080"
    fps: int = 24
    aspect_ratio: str = "16:9"
    target_duration: int = 90
    quality: str = "High"
    seed: Optional[int] = None
    negative_prompt: str = ""
    files: List[str] = Field(default_factory=list)
    render: bool = False


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "ghost-director-studio"}


@app.post("/upload")
def upload_asset(
    project_id: str = Form(...),
    file: UploadFile = File(...),
) -> dict:
    try:
        asset = asset_uploader.save(
            safe_project_id(project_id),
            file.filename or "upload",
            file.content_type or "application/octet-stream",
            file.file,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Upload failed: {exc}") from exc
    finally:
        file.file.close()

    return {"asset": asdict(asset)}


@app.post("/projects")
def create_project(input_data: ProjectInput) -> dict:
    project_id = safe_project_id(input_data.project_id or input_data.title)
    uploaded_assets = asset_uploader.load_manifest(project_id)
    project = Project(
        title=input_data.title,
        project_type=input_data.project_type,
        source_text=input_data.source_text,
        style=input_data.style,
        inputs=input_data.files,
        assets={
            str(asset["id"]): str(asset["path"])
            for asset in uploaded_assets
        },
        metadata={
            "project_id": project_id,
            "uploaded_asset_count": str(len(uploaded_assets)),
            "camera_style": input_data.camera_style,
            "renderer": input_data.renderer,
            "resolution": input_data.resolution,
            "fps": str(input_data.fps),
            "aspect_ratio": input_data.aspect_ratio,
            "target_duration": str(input_data.target_duration),
            "quality": input_data.quality,
            "negative_prompt": input_data.negative_prompt,
        },
    )

    if input_data.seed is not None:
        project.metadata["seed"] = str(input_data.seed)

    try:
        scenes = director.direct_project(
            project,
            run_config=PipelineRunConfig(render=input_data.render),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "project": asdict(project),
        "uploaded_assets": uploaded_assets,
        "scene_count": len(scenes),
        "production_status": asdict(director.production_status(project)),
        "render_queue": [
            asdict(item) for item in director.render_queue(project)
        ],
        "exports": _export_manifest(project),
    }


@app.get("/projects/current/status")
def current_project_status() -> dict:
    try:
        project = director.load_project()
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return asdict(director.production_status(project))


@app.get("/projects/current/render-queue")
def current_render_queue() -> dict:
    try:
        project = director.load_project()
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return {"items": [asdict(item) for item in director.render_queue(project)]}


@app.get("/projects/current/exports")
def current_project_exports() -> dict:
    try:
        project = director.load_project()
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return {"items": _export_manifest(project)}