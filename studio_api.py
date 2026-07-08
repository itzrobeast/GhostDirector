from dataclasses import asdict
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from director import GhostDirector
from pipeline import PipelineRunConfig
from project import Project

app = FastAPI(title="Ghost Director Studio API")
director = GhostDirector()


class ProjectInput(BaseModel):
    title: str = Field(..., min_length=1)
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


@app.post("/projects")
def create_project(input_data: ProjectInput) -> dict:
    project = Project(
        title=input_data.title,
        project_type=input_data.project_type,
        source_text=input_data.source_text,
        style=input_data.style,
        inputs=input_data.files,
        metadata={
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
        "scene_count": len(scenes),
        "production_status": asdict(director.production_status(project)),
        "render_queue": [
            asdict(item) for item in director.render_queue(project)
        ],
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
